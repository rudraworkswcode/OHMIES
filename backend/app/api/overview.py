from fastapi import APIRouter, Depends, Query
from typing import Optional, List, Dict, Any
from app.schemas.auth_schemas import UserProfile
from app.schemas.overview_schemas import OverviewResponse
from app.api.auth import get_current_user
from app.db.supabase_client import db_service
from app.services.consumption import (
    calculate_average_daily_draw,
    calculate_peak_window_intensity
)
from app.services.emissions import calculate_grid_carbon_footprint
from app.services.tariffs import calculate_tariff_bracket
from app.services.recommendations import generate_consumption_summary
from app.core.logging_config import logger

router = APIRouter(prefix="/overview", tags=["Overview"])

@router.get("", response_model=OverviewResponse)
async def get_overview(
    meter_id: Optional[str] = Query(None, description="Optional meter ID to view specific profile"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Returns Tab 1 Overview dashboard metrics and consumption summary.
    Protected endpoint: requires valid authentication token.
    """
    target_meter = meter_id if meter_id else current_user.meter_id
    profile = db_service.get_user_profile(target_meter)
    
    logger.info("Computing Overview metrics for meter: %s (Sector: %s - %s)", target_meter, profile["sector"], profile["subcategory"])
    
    # Fetch consumption records
    df = await db_service.fetch_consumption_records(target_meter, days=30)
    
    # Run calculation services
    daily_draw = calculate_average_daily_draw(df)
    peak_intensity = calculate_peak_window_intensity(df)
    carbon_footprint = calculate_grid_carbon_footprint(df)
    tariff_bracket = calculate_tariff_bracket(df, profile)
    summary = generate_consumption_summary(df, profile)
    
    data_source_label = "Live Supabase Database (RLS)" if db_service.is_configured else "Local Verified Dataset (Deterministic High-Fidelity)"

    return OverviewResponse(
        user={
            "user_id": profile["user_id"],
            "display_name": profile["display_name"],
            "sector": profile["sector"],
            "subcategory": profile["subcategory"],
            "meter_id": profile["meter_id"],
            "goal_kwh_per_week": profile.get("goal_kwh_per_week", 14.5),
            "goal_description": profile.get("goal_description", "Cut 14.5 kWh this week")
        },
        reporting_period=daily_draw.reporting_period or "Last 30 Days",
        total_records_analyzed=len(df),
        data_source=data_source_label,
        average_daily_draw=daily_draw,
        peak_window_intensity=peak_intensity,
        grid_carbon_footprint=carbon_footprint,
        tariff_bracket=tariff_bracket,
        summary=summary
    )

@router.get("/profiles", response_model=List[Dict[str, Any]])
async def list_profiles(current_user: UserProfile = Depends(get_current_user)):
    """Returns available sector archetypes for exploration."""
    return db_service.list_all_archetype_profiles()

