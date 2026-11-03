from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class BattlepassNode(BaseModel):
    week: int
    title: str
    cost_inr: float
    icon: str
    reward_type: str
    description: str
    is_unlocked: bool
    remaining_inr: float

class DomesticSavingsResponse(BaseModel):
    meter_id: str
    streak_weeks: int
    accumulated_savings_inr: float
    weekly_target_cut_kwh: float
    weekly_target_cash_inr: float
    active_tier_label: str
    progress_percentage: float
    roadmap: List[BattlepassNode]
    upcoming_milestone: Optional[BattlepassNode] = None

class CommercialSavingsResponse(BaseModel):
    meter_id: str
    direct_opex_preserved_inr: float
    operating_margin_boost_pct: float
    equivalent_revenue_inr: float
    tod_surcharges_avoided_inr: float
    monthly_baseline_inr: List[float]
    monthly_optimized_inr: List[float]
    cumulative_profit_inr: List[float]
    action_plan: List[str]
    compliance_badge: Dict[str, str]

class SimulationResult(BaseModel):
    target_reduction_pct: float
    monthly_saved_inr: float
    annual_saved_inr: float
    co2_avoided_kg_per_month: float
    equivalent_trees_monthly: float
    baseline_monthly_kwh: float
    reduced_monthly_kwh: float
    applicable_tariff_rate: float

