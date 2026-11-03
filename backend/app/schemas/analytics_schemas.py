from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DailyTrendPoint(BaseModel):
    date: str
    day_name: str
    energy_kwh: float
    rolling_avg_kwh: float
    demand_kw: float

class WeeklyBarPoint(BaseModel):
    week_number: int
    week_label: str
    start_date: str
    end_date: str
    total_kwh: float
    avg_daily_kwh: float
    target_kwh: float
    change_vs_prior_pct: Optional[float] = None

class CategorySlice(BaseModel):
    category: str
    kwh: float
    percentage: float
    color: str
    description: Optional[str] = None

class TimeSlotSlice(BaseModel):
    slot: str
    time_range: str
    kwh: float
    percentage: float
    peak_hour: str

class SmartTipItem(BaseModel):
    id: int
    title: str
    description: str
    rationale: str
    sector: str
    subcategory: str
    estimated_impact: str

class AnalyticsResponse(BaseModel):
    meter_id: str
    sector: str
    subcategory: str
    range_selected: str
    total_energy_kwh: float
    reporting_period: str
    daily_trends: List[DailyTrendPoint]
    weekly_data: List[WeeklyBarPoint]
    equipment_breakdown: List[CategorySlice]
    time_slot_breakdown: List[TimeSlotSlice]
    smart_tips: List[SmartTipItem]

