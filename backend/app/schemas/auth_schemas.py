from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    user_id: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    display_name: str
    sector: str
    subcategory: str
    goal_description: Optional[str] = None

class UserProfile(BaseModel):
    user_id: str
    display_name: str
    sector: str
    subcategory: str
    meter_id: str
    goal_kwh_per_week: Optional[float] = 14.5
    goal_description: Optional[str] = "Cut 14.5 kWh this week"

