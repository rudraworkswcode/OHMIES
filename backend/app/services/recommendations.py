import pandas as pd
from typing import Dict, Any, List
from app.schemas.overview_schemas import ConsumptionSummary
from app.services.consumption import (
    calculate_average_daily_draw,
    calculate_peak_window_intensity,
    calculate_consumption_trend
)

# Smart Tips catalogue mapped by subcategory from sample.md
SECTOR_RECOMMENDATIONS_CATALOGUE: Dict[str, List[str]] = {
    # Domestic
    "High-Rise Apartments": [
        "Set dual inverter AC temperature to 24°C–26°C instead of 18°C–20°C to conserve up to 18% in HVAC draw.",
        "Shift washing machine and high-power dishwashing cycles out of the 7:00 PM – 11:30 PM peak window.",
        "Ensure balcony lighting and ambient fixtures are fitted with 9W or lower LED alternatives."
    ],
    "Independent Bungalows": [
        "Audit garden floodlights and external security lamps; install photocell daylight sensors.",
        "Optimize water booster pump and geyser schedules using digital automated timers.",
        "Consider grid-interactive rooftop solar PV to offset daytime continuous base cooling loads."
    ],
    "Compact Studio or Shared Accommodation": [
        "Eliminate standby phantom vampire draw by unplugging gaming rigs and charging docks when away.",
        "Defrost compact refrigerator coils regularly to maintain compressor thermodynamic efficiency.",
        "Leverage natural daylighting through window blinds during daytime work hours."
    ],
    # Commercial MICRO
    "Flour Mill": [
        "Avoid running heavy pulverizer motors idle during intermittent grain bag loading intervals.",
        "Schedule primary milling runs in off-peak night/morning windows to capture utility tariff rebates.",
        "Check belt tension and motor power factor to eliminate reactive inductive penalties."
    ],
    "Garment and Tailor": [
        "De-energize electric steam irons and sewing machine stations during employee break hours.",
        "Stagger startup times for high-power pressing units to prevent kVA maximum demand spikes.",
        "Upgrade workspace fluorescent tubes to high-efficiency LED batten fittings."
    ],
    "Salon and Wellness": [
        "Maintain water heaters and salon blowers; flush boiler tanks to prevent mineral scale build-up.",
        "Use zonal AC cooling so treatment rooms are only air-conditioned when actively occupied.",
        "Power down UV sanitizers and wax warmers promptly at evening closing."
    ],
    # Commercial SMALL
    "Auto Garage": [
        "Inspect pneumatic air compressor lines for air leaks; a single 3mm leak wastes ~4 kWh/day.",
        "Switch off heavy hydraulic vehicle lift hydraulic pumps when vehicles are securely on stands.",
        "Utilize localized LED task lighting rather than illuminating entire workshop bays."
    ],
    "Photo Studio": [
        "Turn off high-output strobe modeling lamps and studio floodlights between shooting sessions.",
        "Enable energy-saving sleep profiles on high-performance editing workstations and rendering rigs.",
        "Consolidate daily print jobs to run in continuous batches rather than intermittent cycles."
    ],
    "Commercial Bakery": [
        "Execute oven pre-heating strictly within 30 minutes of baking schedules, avoiding prolonged idle heat.",
        "Inspect silicone thermal door gaskets on deck ovens to eliminate 10% radiated convection heat loss.",
        "Interlock kitchen exhaust fans with variable frequency drives (VFD) to adjust airflow to oven usage."
    ],
    # Commercial MEDIUM
    "IT / Co-working Space": [
        "Enforce automated night-time power down scripts on idle workstation monitors and conference AV displays.",
        "Optimize server room HVAC setpoints to ASHRAE standards (22°C–24°C) instead of excessive 18°C over-cooling.",
        "Program chiller plants to pre-cool facilities before morning peak electricity tariff windows."
    ],
    "Retail Showroom": [
        "Automate showroom perimeter display and decorative sign lighting to extinguish 30 minutes after closing.",
        "Install motion occupancy sensors in customer fitting rooms, back-office storage, and restrooms.",
        "Utilize LED track spotlights with high CRI and low heat dissipation to minimize AC load."
    ],
    "24/7 Cold Pharmacy": [
        "Verify magnetic door seals and air curtains on medical refrigeration units to prevent temperature leakage.",
        "Ensure adequate 150mm ventilation clearance around refrigeration condenser coils to optimize heat rejection.",
        "Schedule automated defrost heating cycles during early morning off-peak tariff hours (2:00 AM – 4:00 AM)."
    ]
}

def generate_consumption_summary(
    df: pd.DataFrame,
    profile: Dict[str, Any]
) -> ConsumptionSummary:
    """
    Generates an intelligent, transparent consumption summary derived strictly
    from dataset statistics as required by PRD section 4.
    """
    subcategory = profile.get("subcategory", "High-Rise Apartments")
    sector = profile.get("sector", "Domestic")
    user_name = profile.get("display_name", "User")
    
    if df.empty:
        return ConsumptionSummary(
            headline="No consumption records found for this meter profile.",
            current_consumption_kwh=0.0,
            daily_average_kwh=0.0,
            peak_window="N/A",
            trend_direction="steady",
            trend_percentage=0.0,
            comparison_text="Data currently unavailable. Please check meter connection.",
            actionable_recommendations=["Connect smart meter to begin consumption analysis."],
            statistical_details={}
        )

    unique_days = int(df["date"].nunique())
    total_kwh = float(df["energy_kwh"].sum())
    daily_avg_kwh = total_kwh / max(1, unique_days)
    
    daily_draw_metric = calculate_average_daily_draw(df)
    peak_metric = calculate_peak_window_intensity(df)
    direction, trend_pct = calculate_consumption_trend(df)

    # Weekend vs Weekday analysis
    df["weekday"] = pd.to_datetime(df["timestamp"]).dt.weekday
    weekend_days = df[df["weekday"] >= 5]["date"].nunique()
    weekday_days = df[df["weekday"] < 5]["date"].nunique()

    weekend_kwh = df[df["weekday"] >= 5]["energy_kwh"].sum()
    weekday_kwh = df[df["weekday"] < 5]["energy_kwh"].sum()

    avg_weekend_daily = (weekend_kwh / max(1, weekend_days)) if weekend_days > 0 else daily_avg_kwh
    avg_weekday_daily = (weekday_kwh / max(1, weekday_days)) if weekday_days > 0 else daily_avg_kwh
    weekend_ratio = avg_weekend_daily / max(0.1, avg_weekday_daily)

    # Night ratio (11 PM - 6 AM)
    night_kwh = df[df["hour"].isin([23, 0, 1, 2, 3, 4, 5])]["energy_kwh"].sum()
    night_ratio = night_kwh / max(0.1, total_kwh)

    # Narrative construction
    if direction == "decreasing":
        trend_clause = f"decreasing by {trend_pct}% compared to the prior baseline period"
    elif direction == "increasing":
        trend_clause = f"trending higher by {trend_pct}% compared to the prior baseline period"
    else:
        trend_clause = f"holding steady with less than 2.5% variation"

    headline = (
        f"{user_name}'s consumption is averaging {daily_avg_kwh:.1f} kWh/day "
        f"across the last {unique_days} days, {trend_clause}."
    )

    comparison_text = (
        f"Your peak intensity is concentrated between {peak_metric.window} "
        f"(averaging {peak_metric.energy_kwh:.1f} kWh cumulative draw with peak instantaneous power at {peak_metric.demand_kw:.1f} kW). "
        f"Weekend usage is {weekend_ratio:.2f}x of weekday levels, with {night_ratio*100:.1f}% consumed during night hours."
    )

    # Select recommendations
    recommendations = SECTOR_RECOMMENDATIONS_CATALOGUE.get(
        subcategory,
        SECTOR_RECOMMENDATIONS_CATALOGUE["High-Rise Apartments"]
    )

    statistical_details = {
        "unique_days_analyzed": unique_days,
        "total_energy_kwh": round(total_kwh, 2),
        "daily_average_kwh": round(daily_avg_kwh, 2),
        "peak_window": peak_metric.window,
        "peak_demand_kw": peak_metric.demand_kw,
        "peak_energy_kwh": peak_metric.energy_kwh,
        "weekend_ratio": round(weekend_ratio, 2),
        "night_consumption_share_pct": round(night_ratio * 100.0, 1),
        "trend_direction": direction,
        "trend_percentage": trend_pct
    }

    return ConsumptionSummary(
        headline=headline,
        current_consumption_kwh=round(total_kwh, 1),
        daily_average_kwh=round(daily_avg_kwh, 1),
        peak_window=peak_metric.window,
        trend_direction=direction,
        trend_percentage=trend_pct,
        comparison_text=comparison_text,
        actionable_recommendations=recommendations,
        statistical_details=statistical_details
    )

