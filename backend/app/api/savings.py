from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.schemas.auth_schemas import UserProfile
from app.schemas.savings_schemas import (
    DomesticSavingsResponse,
    CommercialSavingsResponse,
    SimulationResult
)
from app.api.auth import get_current_user
from app.db.supabase_client import db_service
from app.services.savings_service import (
    build_domestic_greenpass,
    build_commercial_financials,
    run_simulation
)
from app.core.logging_config import logger

router = APIRouter(prefix="/savings", tags=["Savings (Phase 3)"])

@router.get("/domestic", response_model=DomesticSavingsResponse)
async def get_domestic_savings(
    meter_id: Optional[str] = Query(None, description="Optional meter identifier"),
    streak: Optional[int] = Query(None, ge=1, le=52, description="Simulated streak weeks"),
    current_user: UserProfile = Depends(get_current_user)
):
    """Returns Green Pass Road battlepass milestones and bank savings progression."""
    target_meter = meter_id if meter_id else current_user.meter_id
    profile = db_service.get_user_profile(target_meter)
    logger.info("Computing Green Pass Road for meter: %s (Streak: %s)", target_meter, streak)
    return build_domestic_greenpass(profile, streak_weeks=streak)

@router.get("/commercial", response_model=CommercialSavingsResponse)
async def get_commercial_savings(
    meter_id: Optional[str] = Query(None, description="Optional commercial meter identifier"),
    peak_shift: float = Query(25.0, ge=0.0, le=60.0, description="Peak load shift percentage"),
    current_user: UserProfile = Depends(get_current_user)
):
    """Returns commercial OPEX preservation, EBITDA margin expansion, and financial curves."""
    target_meter = meter_id if meter_id else current_user.meter_id
    profile = db_service.get_user_profile(target_meter)
    logger.info("Computing Commercial Financials for meter: %s (Peak Shift: %.1f%%)", target_meter, peak_shift)
    return build_commercial_financials(profile, peak_shift_pct=peak_shift)

@router.get("/simulate", response_model=SimulationResult)
async def simulate_savings(
    meter_id: Optional[str] = Query(None, description="Optional meter identifier"),
    reduction_pct: float = Query(15.0, ge=5.0, le=40.0, description="Target reduction percentage"),
    current_user: UserProfile = Depends(get_current_user)
):
    """Interactive What-If reduction simulator with transparent financial and emissions math."""
    target_meter = meter_id if meter_id else current_user.meter_id
    profile = db_service.get_user_profile(target_meter)
    df = await db_service.fetch_consumption_records(target_meter, days=30)
    return run_simulation(df, profile, target_reduction_pct=reduction_pct)
