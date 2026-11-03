from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class MetricValue(BaseModel):
    value: float
    unit: str
    reporting_period: Optional[str] = None
    subtext: Optional[str] = None

class PeakIntensityMetric(BaseModel):
    energy_kwh: float
    demand_kw: float
    window: str
    unit_energy: str = "kWh"
    unit_demand: str = "kW"
    peak_hour: str
    distinction_note: str = "Distinguishing cumulative energy (kWh) from instantaneous demand (kW)"

class CarbonFootprintMetric(BaseModel):
    total_emissions_kg_co2e: float
    daily_emissions_kg_co2e: float
    emission_factor_kg_per_kwh: float
    factor_source: str
    equivalent_trees_offset_per_month: float

class TariffBracketMetric(BaseModel):
    tariff_category: str
    average_effective_rate_inr: float
    unit: str = "INR / kWh"
    slab_structure: str
    fixed_charge_inr: float
    estimated_daily_cost_inr: float

class ConsumptionSummary(BaseModel):
    headline: str
    current_consumption_kwh: float
    daily_average_kwh: float
    peak_window: str
    trend_direction: str  # "increasing", "decreasing", "steady"
    trend_percentage: float
    comparison_text: str
    actionable_recommendations: List[str]
    statistical_details: Dict[str, Any]

class OverviewResponse(BaseModel):
    user: Dict[str, Any]
    reporting_period: str
    total_records_analyzed: int
    data_source: str
    average_daily_draw: MetricValue
    peak_window_intensity: PeakIntensityMetric
    grid_carbon_footprint: CarbonFootprintMetric
    tariff_bracket: TariffBracketMetric
    summary: ConsumptionSummary

