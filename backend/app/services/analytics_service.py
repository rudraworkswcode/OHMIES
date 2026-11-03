import pandas as pd
import numpy as np
from typing import Dict, Any, List
from app.schemas.analytics_schemas import (
    DailyTrendPoint,
    WeeklyBarPoint,
    CategorySlice,
    TimeSlotSlice,
    SmartTipItem,
    AnalyticsResponse
)

# Realistic sector equipment load proportions
EQUIPMENT_PROFILES = {
    "High-Rise Apartments": [
        ("Inverter Split ACs (HVAC)", 0.42, "#10b981", "Dual 1.5 ton cooling units"),
        ("Refrigeration & Deep Chill", 0.18, "#06b6d4", "Frost-free 350L refrigerator"),
        ("Water Heating & Geysers", 0.15, "#f59e0b", "Storage water heaters 25L"),
        ("Kitchen & Induction", 0.15, "#6366f1", "Induction stove & microwaves"),
        ("Lighting & Standby", 0.10, "#a855f7", "LED lamps and smart devices")
    ],
    "Independent Bungalows": [
        ("Central Cooling & Ducted AC", 0.48, "#10b981", "Multi-zone air conditioning"),
        ("Water Pumps & Filtration", 0.18, "#06b6d4", "Borewell & pressure booster pumps"),
        ("Refrigeration & Freezers", 0.14, "#f59e0b", "Multi-door refrigerators"),
        ("Outdoor & Security Lighting", 0.12, "#6366f1", "Perimeter security lights"),
        ("Kitchen & Laundry", 0.08, "#a855f7", "Heavy duty washers & ovens")
    ],
    "Compact Studio or Shared Accommodation": [
        ("Single AC / Climate Control", 0.35, "#10b981", "1 Ton split air conditioner"),
        ("Computing & Workstations", 0.28, "#06b6d4", "Dual monitor rigs and gaming PCs"),
        ("Compact Refrigeration", 0.18, "#f59e0b", "Single-door 190L refrigerator"),
        ("Instant Geyser", 0.12, "#6366f1", "3kW bathroom instant geyser"),
        ("Standby / Vampire Load", 0.07, "#a855f7", "Chargers and smart gadgets")
    ],
    "Flour Mill": [
        ("Main Grinding 15HP Motor", 0.64, "#10b981", "Heavy induction milling motor"),
        ("Pulverizer & Rotary Sifter", 0.18, "#06b6d4", "Fine spice and grain screening"),
        ("Exhaust Blowers & Dust Intake", 0.10, "#f59e0b", "Continuous dust collection"),
        ("Facility Lighting & Controls", 0.08, "#6366f1", "Lighting and control panels")
    ],
    "Commercial Bakery": [
        ("Deck Ovens & Heating Elements", 0.58, "#10b981", "Three-deck baking chambers"),
        ("Spiral Dough Mixers & Kneaders", 0.16, "#06b6d4", "Heavy industrial planetary mixers"),
        ("Exhaust Hoods & Heat Dissipation", 0.14, "#f59e0b", "Variable speed kitchen extractors"),
        ("Proofing Chambers & Lighting", 0.12, "#6366f1", "Humidity proofer and prep bay lights")
    ],
    "24/7 Cold Pharmacy": [
        ("Vaccine & Insulin Deep Freezers", 0.52, "#10b981", "-20°C calibrated medical chillers"),
        ("Retail Cold Display Cabinets", 0.22, "#06b6d4", "Glass-front beverage & serum coolers"),
        ("Storefront HVAC & Ambience", 0.18, "#f59e0b", "24/7 retail customer area AC"),
        ("Inverter UPS Buffer System", 0.08, "#6366f1", "Battery charging & emergency standby")
    ]
}

DEFAULT_EQUIPMENT = [
    ("Primary Baseload Machinery", 0.45, "#10b981", "Core operations"),
    ("Secondary Equipment", 0.25, "#06b6d4", "Auxiliary processes"),
    ("Thermal & Climate Control", 0.18, "#f59e0b", "Heating and ventilation"),
    ("Lighting & Office Utilities", 0.12, "#6366f1", "Ambient fixtures and office draw")
]

def build_analytics_data(
    df: pd.DataFrame,
    profile: Dict[str, Any],
    range_filter: str = "30d"
) -> AnalyticsResponse:
    """
    Computes daily trends with rolling averages, weekly bar charts,
    pie chart category distributions, and tailored smart tips.
    """
    meter_id = profile.get("meter_id", "DOM-9821")
    sector = profile.get("sector", "Domestic")
    subcategory = profile.get("subcategory", "High-Rise Apartments")

    if df.empty:
        return AnalyticsResponse(
            meter_id=meter_id,
            sector=sector,
            subcategory=subcategory,
            range_selected=range_filter,
            total_energy_kwh=0.0,
            reporting_period="No data",
            daily_trends=[],
            weekly_data=[],
            equipment_breakdown=[],
            time_slot_breakdown=[],
            smart_tips=[]
        )

    # 1. Daily Aggregations & Rolling 7-day Average
    daily_df = df.groupby("date").agg({
        "energy_kwh": "sum",
        "demand_kw": "max",
        "timestamp": "first"
    }).reset_index().sort_values("date")

    daily_df["rolling_avg_kwh"] = daily_df["energy_kwh"].rolling(window=7, min_periods=1).mean().round(2)
    daily_df["day_name"] = pd.to_datetime(daily_df["date"]).dt.strftime("%a")

    # Filter based on selected date range
    if range_filter == "7d":
        filtered_daily = daily_df.tail(7)
    elif range_filter == "14d":
        filtered_daily = daily_df.tail(14)
    else:
        filtered_daily = daily_df

    daily_points: List[DailyTrendPoint] = []
    for _, row in filtered_daily.iterrows():
        daily_points.append(DailyTrendPoint(
            date=str(row["date"]),
            day_name=str(row["day_name"]),
            energy_kwh=round(float(row["energy_kwh"]), 2),
            rolling_avg_kwh=round(float(row["rolling_avg_kwh"]), 2),
            demand_kw=round(float(row["demand_kw"]), 2)
        ))

    # 2. Weekly Bar Chart Data (Consistent 7-day Bins)
    weekly_bars: List[WeeklyBarPoint] = []
    num_days = len(daily_df)
    target_weekly = profile.get("base_daily_kwh", 18.0) * 7.0 * 0.90  # 10% below baseline

    for w_idx in range(4):
        start_idx = w_idx * 7
        end_idx = min(num_days, start_idx + 7)
        if start_idx >= num_days:
            break
        week_slice = daily_df.iloc[start_idx:end_idx]
        if week_slice.empty:
            continue

        week_kwh = float(week_slice["energy_kwh"].sum())
        week_days = len(week_slice)
        avg_d = week_kwh / max(1, week_days)
        start_d = str(week_slice["date"].min())
        end_d = str(week_slice["date"].max())
        
        # Calculate % change vs previous week if available
        change_pct = None
        if w_idx > 0 and len(weekly_bars) > 0:
            prior_kwh = weekly_bars[-1].total_kwh
            if prior_kwh > 0:
                change_pct = round(((week_kwh - prior_kwh) / prior_kwh) * 100.0, 1)

        weekly_bars.append(WeeklyBarPoint(
            week_number=w_idx + 1,
            week_label=f"Week {w_idx + 1}",
            start_date=start_d,
            end_date=end_d,
            total_kwh=round(week_kwh, 1),
            avg_daily_kwh=round(avg_d, 2),
            target_kwh=round(target_weekly, 1),
            change_vs_prior_pct=change_pct
        ))

    total_kwh = float(df["energy_kwh"].sum())

    # 3. Time Slot Breakdown (Night, Morning, Afternoon, Evening)
    def assign_slot(hour: int) -> str:
        if 0 <= hour <= 5:
            return "Night"
        elif 6 <= hour <= 11:
            return "Morning"
        elif 12 <= hour <= 17:
            return "Afternoon"
        else:
            return "Evening"

    df["time_slot"] = df["hour"].apply(assign_slot)
    slot_order = ["Night", "Morning", "Afternoon", "Evening"]
    slot_ranges = {
        "Night": "00:00 - 05:59",
        "Morning": "06:00 - 11:59",
        "Afternoon": "12:00 - 17:59",
        "Evening": "18:00 - 23:59"
    }

    slot_breakdown: List[TimeSlotSlice] = []
    slot_grp = df.groupby("time_slot")["energy_kwh"].sum()
    
    for slot in slot_order:
        kwh_val = float(slot_grp.get(slot, 0.0))
        pct = (kwh_val / max(0.1, total_kwh)) * 100.0
        # Peak single hour in this slot
        slot_hours = df[df["time_slot"] == slot]
        peak_h = slot_hours.groupby("hour")["energy_kwh"].mean().idxmax() if not slot_hours.empty else 0

        slot_breakdown.append(TimeSlotSlice(
            slot=slot,
            time_range=slot_ranges[slot],
            kwh=round(kwh_val, 1),
            percentage=round(pct, 1),
            peak_hour=f"{peak_h:02d}:00"
        ))

    # 4. Equipment / Appliance Breakdown
    equip_defs = EQUIPMENT_PROFILES.get(subcategory, DEFAULT_EQUIPMENT)
    equip_breakdown: List[CategorySlice] = []
    for name, share, color, desc in equip_defs:
        kwh = round(total_kwh * share, 1)
        equip_breakdown.append(CategorySlice(
            category=name,
            kwh=kwh,
            percentage=round(share * 100.0, 1),
            color=color,
            description=desc
        ))

    # 5. Smart Tips from Catalogue
    smart_tips = generate_smart_tips(df, profile)

    return AnalyticsResponse(
        meter_id=meter_id,
        sector=sector,
        subcategory=subcategory,
        range_selected=range_filter,
        total_energy_kwh=round(total_kwh, 1),
        reporting_period=f"{daily_df['date'].min()} to {daily_df['date'].max()}",
        daily_trends=daily_points,
        weekly_data=weekly_bars,
        equipment_breakdown=equip_breakdown,
        time_slot_breakdown=slot_breakdown,
        smart_tips=smart_tips
    )

def generate_smart_tips(df: pd.DataFrame, profile: Dict[str, Any]) -> List[SmartTipItem]:
    """Generates predefined Smart Tips tailored to sector and observed data patterns."""
    subcategory = profile.get("subcategory", "High-Rise Apartments")
    sector = profile.get("sector", "Domestic")
    tips: List[SmartTipItem] = []

    # Check observed data patterns
    night_kwh = df[df["hour"].isin([23, 0, 1, 2, 3, 4, 5])]["energy_kwh"].sum()
    total_kwh = df["energy_kwh"].sum()
    night_share = night_kwh / max(0.1, total_kwh)

    df["weekday"] = pd.to_datetime(df["timestamp"]).dt.weekday
    weekend_kwh = df[df["weekday"] >= 5]["energy_kwh"].mean()
    weekday_kwh = df[df["weekday"] < 5]["energy_kwh"].mean()
    weekend_surge = (weekend_kwh > weekday_kwh * 1.15) if weekday_kwh else False

    if sector == "Domestic":
        tips.append(SmartTipItem(
            id=1,
            title="Thermostat Setpoint Optimization (24°C–26°C)",
            description="Raise split AC temperatures from 18°C–20°C to 24°C–26°C with ceiling fan circulation.",
            rationale="Cooling accounts for over 40% of residential energy draw. Each 1°C increase conserves ~6% compressor power.",
            sector=sector,
            subcategory=subcategory,
            estimated_impact="Save ~12–18% on monthly HVAC bill"
        ))
        tips.append(SmartTipItem(
            id=2,
            title="Shift High-Load Appliances from Peak Evening",
            description="Run automatic washing machines, dishwashers, and ironing before 6:00 PM or after 10:30 PM.",
            rationale="Evening hours (7:00 PM – 11:00 PM) show your highest load intensity.",
            sector=sector,
            subcategory=subcategory,
            estimated_impact="Reduces peak grid strain and avoids upper slab escalation"
        ))
        if night_share > 0.20:
            tips.append(SmartTipItem(
                id=3,
                title="Mitigate Overnight Standby & Sleep Timers",
                description="Set 3-hour sleep timers on bedroom AC units and power down unneeded entertainment docks.",
                rationale=f"Observed night draw represents {night_share*100:.1f}% of total energy consumption.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Save ~8–12 kWh per week"
            ))
        else:
            tips.append(SmartTipItem(
                id=3,
                title="Daylight Harvesting & LED Transition",
                description="Use natural morning daylighting in living areas and replace any remaining halogen downlights with 9W LEDs.",
                rationale="Lighting accounts for ~10% of auxiliary apartment load.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Save ~4–6 kWh per month per fixture"
            ))
    else:
        # Commercial Smart Tips
        if subcategory == "Flour Mill":
            tips.append(SmartTipItem(
                id=1,
                title="Off-Peak Coarse Milling Runs",
                description="Shift primary coarse grain crushing cycles to the utility night rebate window (11:00 PM – 6:00 AM).",
                rationale="Commercial ToD tariff grants a ₹1.00/kWh discount during off-peak hours.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Recover ~₹4,500 – ₹7,000 monthly in ToD rebates"
            ))
            tips.append(SmartTipItem(
                id=2,
                title="Motor Power Factor & Belt Tension Audit",
                description="Inspect 15HP induction motor capacitors to maintain power factor above 0.95 PF and tension V-belts.",
                rationale="Eliminates reactive inductive penalties and motor heating slip loss.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Prevents ~₹1,200 monthly utility low-PF penalty"
            ))
            tips.append(SmartTipItem(
                id=3,
                title="Staggered Motor Startups",
                description="Never start multiple pulverizer motors simultaneously; maintain a 60-second start interval.",
                rationale="Instant inrush current creates kVA maximum demand spikes on the utility bill.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Prevents exceeding contract demand limit"
            ))
        elif subcategory == "Commercial Bakery":
            tips.append(SmartTipItem(
                id=1,
                title="Night-Hour Preheating Schedule",
                description="Pre-heat commercial deck ovens strictly during the 3:00 AM – 5:30 AM night tariff window.",
                rationale="Captures night concession tariff rates for the heaviest thermal warm-up cycle.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Save ~₹3,500 monthly on preheating OPEX"
            ))
            tips.append(SmartTipItem(
                id=2,
                title="Thermal Door Gasket Replacement",
                description="Inspect silicone perimeter seals on baking oven doors for heat leakage.",
                rationale="Compromised door gaskets cause 8–10% continuous radiated heat loss.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Recovers ~15 kWh daily in wasted heat"
            ))
            tips.append(SmartTipItem(
                id=3,
                title="Variable Speed Kitchen Exhaust VFD",
                description="Interlock ventilation hood fans with temperature sensors or VFD drives instead of fixed 100% speed.",
                rationale="Exhaust ventilation runs continuously even during non-baking prep periods.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Cut ~20% auxiliary blower energy"
            ))
        else:
            # Cold Pharmacy / Generic Commercial
            tips.append(SmartTipItem(
                id=1,
                title="Condenser Coil Spacing & Defrost Timers",
                description="Maintain 150mm clearance around medical chiller condenser coils and set automated defrost at 2:00 AM.",
                rationale="Refrigeration runs 24/7; restricted airflow forces compressors to cycle 25% longer.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Save ~18–25 kWh/week on critical chiller loop"
            ))
            tips.append(SmartTipItem(
                id=2,
                title="Retail Showcase vs Cold Chain Circuit Isolation",
                description="Segregate decorative retail showcase display lighting from critical vaccine freezer circuits.",
                rationale="Prevents unneeded display fixtures from drawing power during closed hours.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Eliminate ~14 kWh daily in off-hours lighting"
            ))
            tips.append(SmartTipItem(
                id=3,
                title="Door Magnetic Seal Inspection",
                description="Inspect magnetic seals on medicine deep freezers using the paper test to prevent cold air leakage.",
                rationale="Ensures strict compliance with medical storage standards while minimizing compressor load.",
                sector=sector,
                subcategory=subcategory,
                estimated_impact="Protects drug inventory and cuts compressor run-time"
            ))

    return tips

