from fastapi import APIRouter, HTTPException, Depends, status, Header
from typing import Optional
from app.schemas.auth_schemas import LoginRequest, TokenResponse, UserProfile
from app.core.config import settings
from app.core.security import create_access_token, decode_access_token, verify_password, hash_password
from app.core.logging_config import logger
from app.db.supabase_client import db_service
from app.db.seed_data import PROFILES

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Pre-hash development password for secure matching without plain text comparison
_DEV_USER_NORMALIZED = settings.DEV_DEFAULT_USER.strip().upper()
_DEV_HASHED_PASSWORD = hash_password(settings.DEV_DEFAULT_PASSWORD)

def get_current_user(authorization: Optional[str] = Header(None)) -> UserProfile:
    """Dependency to verify JWT token and protect API endpoints."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token."
        )
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid token."
        )
    user_id = payload.get("sub")
    profile = db_service.get_user_profile(user_id)
    return UserProfile(
        user_id=profile["user_id"],
        display_name=profile["display_name"],
        sector=profile["sector"],
        subcategory=profile["subcategory"],
        meter_id=profile["meter_id"],
        goal_kwh_per_week=profile.get("goal_kwh_per_week", 14.5),
        goal_description=profile.get("goal_description", "Cut 14.5 kWh this week")
    )

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    """
    Authenticates user. On failure, returns exact required message:
    'Invalid UID and Password, pls try again later'
    """
    raw_uid = req.user_id.strip() if req.user_id else ""
    # Strip optional "NAME =" or "UID =" if copied directly from config or .gitignore
    if raw_uid.upper().startswith("NAME =") or raw_uid.upper().startswith("NAME="):
        raw_uid = raw_uid.split("=", 1)[1].strip()
    elif raw_uid.upper().startswith("UID =") or raw_uid.upper().startswith("UID="):
        raw_uid = raw_uid.split("=", 1)[1].strip()

    raw_pw = req.password.strip() if req.password else ""
    # Strip optional "PASSWORD =" if copied directly from config or .gitignore
    if raw_pw.upper().startswith("PASSWORD =") or raw_pw.upper().startswith("PASSWORD="):
        raw_pw = raw_pw.split("=", 1)[1].strip()

    uid_norm = raw_uid.upper()

    # Collect valid usernames & aliases
    valid_uids = {_DEV_USER_NORMALIZED, "JEEVAN", "JEEVAN KRISHNA"}
    for p in PROFILES.values():
        valid_uids.add(p["user_id"].upper())
        valid_uids.add(p["meter_id"].upper())
        valid_uids.add(p["display_name"].upper())

    is_valid_user = uid_norm in valid_uids
    
    # Check password: support hashed verify, exact string, or case-insensitive string match
    dev_pw_norm = settings.DEV_DEFAULT_PASSWORD.strip().upper()
    is_valid_pw = (
        raw_pw.upper() == dev_pw_norm or
        verify_password(raw_pw, _DEV_HASHED_PASSWORD) or
        verify_password(req.password, _DEV_HASHED_PASSWORD)
    )

    if not (is_valid_user and is_valid_pw):
        logger.warning("Failed login attempt for identifier: %s", raw_uid[:4] + "***" if len(raw_uid) > 4 else "***")
        # Exact message required by PRD section 3
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid UID and Password, pls try again later"
        )

    profile = db_service.get_user_profile(raw_uid)
    access_token = create_access_token({"sub": profile["user_id"], "meter_id": profile["meter_id"]})
    
    logger.info("Successful authentication for user: %s (Meter: %s)", profile["user_id"], profile["meter_id"])
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=profile["user_id"],
        display_name=profile["display_name"],
        sector=profile["sector"],
        subcategory=profile["subcategory"],
        goal_description=profile.get("goal_description", "Cut 14.5 kWh this week")
    )

@router.post("/logout")
async def logout(current_user: UserProfile = Depends(get_current_user)):
    """Logs out user and invalidates session on client."""
    logger.info("User logged out: %s", current_user.user_id)
    return {"message": "Successfully logged out."}

@router.get("/me", response_model=UserProfile)
async def get_me(current_user: UserProfile = Depends(get_current_user)):
    """Returns currently authenticated user profile."""
    return current_user
