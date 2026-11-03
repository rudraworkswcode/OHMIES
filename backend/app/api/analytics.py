from fastapi import APIRouter, Depends, Query
from typing import Optional, List
import pandas as pd
from app.schemas.auth_schemas import UserProfile
from app.schemas.analytics_schemas import AnalyticsResponse, SmartTipItem
from app.api.auth import get_current_user
from app.db.supabase_client import db_service
from app.services.analytics_service import build_analytics_data, generate_smart_tips
from app.core.logging_config import logger

router = APIRouter(prefix="/analytics", tags=["Analytics (Phase 2)"])

@router.get("/consumption", response_model=AnalyticsResponse)
async def get_analytics_consumption(
    meter_id: Optional[str] = Query(None, description="Optional meter identifier"),
    range: str = Query("30d", pattern="^(7d|14d|30d)$", description="Date range: 7d, 14d, or 30d"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Returns Phase 2 historical consumption trends, weekly bar chart data,
    time-slot / equipment category breakdown for pie charts, and smart tips.
    """
    target_meter = meter_id if meter_id else current_user.meter_id
    profile = db_service.get_user_profile(target_meter)
    logger.info("Serving Analytics data for meter %s, range %s", target_meter, range)

    df = await db_service.fetch_consumption_records(target_meter, days=30)
    data = build_analytics_data(df, profile, range_filter=range)
    return data

@router.get("/tips", response_model=List[SmartTipItem])
async def get_smart_tips_list(
    meter_id: Optional[str] = Query(None, description="Optional meter identifier"),
    current_user: UserProfile = Depends(get_current_user)
):
    """Returns sector- and subcategory-matched smart tips."""
    target_meter = meter_id if meter_id else current_user.meter_id
    profile = db_service.get_user_profile(target_meter)
    df = await db_service.fetch_consumption_records(target_meter, days=30)
    return generate_smart_tips(df, profile)
