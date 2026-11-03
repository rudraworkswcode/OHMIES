import pandas as pd
from typing import Dict, Any, List, Optional
from app.schemas.savings_schemas import (
    BattlepassNode,
    DomesticSavingsResponse,
    CommercialSavingsResponse,
    SimulationResult
)
from app.services.tariffs import calculate_tariff_bracket

# Battlepass milestone schema from volt site concept 3.html
BATTLEPASS_ROAD_DEFINITIONS = [
    {
        "week": 1,
        "title": "Artisanal Barista Coffee & Snack",
        "cost_inr": 180.0,
        "icon": "☕",
        "reward_type": "Micro-Treat",
        "description": "First conservation goal met! Enough electricity cost eliminated to fund your favorite barista roast."
    },
    {
        "week": 2,
        "title": "Cinema Screening & Gourmet Popcorn",
        "cost_inr": 420.0,
        "icon": "🎬",
        "reward_type": "Micro-Treat",
        "description": "Two weeks strong. Covers a blockbuster multiplex ticket and refreshments with zero out-of-pocket spend."
    },
    {
        "week": 4,
        "title": "Ionic Quick-Dry Salon Hair Dryer",
        "cost_inr": 820.0,
        "icon": "💨",
        "reward_type": "Personal Appliance",
        "description": "Month 1 cleared. Total power expense eliminated covers the full retail price of this high-efficiency grooming tool."
    },
    {
        "week": 8,
        "title": "ANC Wireless Bluetooth Earbuds",
        "cost_inr": 1950.0,
        "icon": "🎧",
        "reward_type": "Personal Tech",
        "description": "Two full months of cluster savings pays for wireless active noise cancelling audio earbuds."
    },
    {
        "week": 12,
        "title": "Fine Dining Gourmet Dinner for Two",
        "cost_inr": 3200.0,
        "icon": "🍽️",
        "reward_type": "Lifestyle Experience",
        "description": "Quarter 1 Champion. A celebratory multi-course dinner fully sponsored by your reduced electricity bill."
    },
    {
        "week": 24,
        "title": "Weekend Luxury Resort Stay",
        "cost_inr": 6500.0,
        "icon": "🏨",
        "reward_type": "Getaway Escape",
        "description": "Half-year milestone. A weekend countryside retreat accommodation completely funded by cumulative grid savings."
    },
    {
        "week": 52,
        "title": "Round-Trip Flight Tickets & Vacation",
        "cost_inr": 14500.0,
        "icon": "✈️",
        "reward_type": "Grand Vacation (Final Boss)",
        "description": "Full 1-Year Conservation Master. A round-trip beach getaway escape funded purely by zero-waste energy habits!"
    }
]

def build_domestic_greenpass(
    profile: Dict[str, Any],
    streak_weeks: Optional[int] = None
) -> DomesticSavingsResponse:
    """Computes Battle Pass nodes and accumulated bank savings for domestic users."""
    meter_id = profile.get("meter_id", "DOM-9821")
    current_streak = streak_weeks if streak_weeks is not None else int(profile.get("streak_weeks", 3))
    
    # Target savings per week in kWh & cash
    target_cut_kwh = float(profile.get("goal_kwh_per_week", 14.5))
    tariff_rate = float(profile.get("tariff_base_rate", 8.50))
    weekly_cash = round(target_cut_kwh * tariff_rate, 0)

    accumulated_savings = current_streak * weekly_cash

    roadmap: List[BattlepassNode] = []
    upcoming_milestone: Optional[BattlepassNode] = None

    for item in BATTLEPASS_ROAD_DEFINITIONS:
        cost = item["cost_inr"]
        is_unlocked = accumulated_savings >= cost
        remaining = max(0.0, cost - accumulated_savings)

        node = BattlepassNode(
            week=item["week"],
            title=item["title"],
            cost_inr=cost,
            icon=item["icon"],
            reward_type=item["reward_type"],
            description=item["description"],
            is_unlocked=is_unlocked,
            remaining_inr=remaining
        )
        roadmap.append(node)

        if not is_unlocked and upcoming_milestone is None:
            upcoming_milestone = node

    # Progress percentage toward the 52-week ultimate target
    max_cost = BATTLEPASS_ROAD_DEFINITIONS[-1]["cost_inr"]
    progress_pct = min(100.0, round((accumulated_savings / max_cost) * 100.0, 1))

    return DomesticSavingsResponse(
        meter_id=meter_id,
        streak_weeks=current_streak,
        accumulated_savings_inr=accumulated_savings,
        weekly_target_cut_kwh=target_cut_kwh,
        weekly_target_cash_inr=weekly_cash,
        active_tier_label=f"Tier: Week {current_streak} In Progress",
        progress_percentage=progress_pct,
        roadmap=roadmap,
        upcoming_milestone=upcoming_milestone or roadmap[-1]
    )

def build_commercial_financials(
    profile: Dict[str, Any],
    peak_shift_pct: float = 25.0
) -> CommercialSavingsResponse:
    """Computes commercial OPEX reductions, EBITDA boost, ToD penalties avoided, and charts."""
    meter_id = profile.get("meter_id", "COM-7714")
    subcategory = profile.get("subcategory", "Flour Mill")
    base_daily_kwh = float(profile.get("base_daily_kwh", 54.0))
    tariff_rate = float(profile.get("tariff_base_rate", 10.50))

    monthly_base_spend = base_daily_kwh * 30.0 * tariff_rate
    
    # Financial KPI multipliers
    shift_ratio = peak_shift_pct / 100.0
    direct_opex = round(monthly_base_spend * (0.10 + shift_ratio * 0.12), 0)
    operating_margin_boost = round(1.2 + (shift_ratio * 3.5), 2)
    equivalent_revenue = round(direct_opex * 10.0, 0)
    tod_avoided = round(direct_opex * 0.22, 0)

    # 6-Month trajectory curves
    monthly_baseline = [round(monthly_base_spend, 0)] * 6
    monthly_optimized = [
        round(monthly_base_spend * (1.0 - (0.04 * (i + 1))), 0) for i in range(6)
    ]
    cumulative_profit = []
    running_sum = 0.0
    for b, o in zip(monthly_baseline, monthly_optimized):
        running_sum += (b - o)
        cumulative_profit.append(round(running_sum, 0))

    action_plans = {
        "Flour Mill": [
            "Shift primary grain pulverizing run to the 11:00 PM – 6:00 AM off-peak window to capture ₹1.80/unit rebate.",
            "Install automatic power factor correction capacitors to eliminate ₹1,200/month low-PF surcharge.",
            "Stagger startup times on 15HP induction motors to avoid instantaneous kVA peak demand surcharges."
        ],
        "Commercial Bakery": [
            "Execute primary deck oven preheating during the 3:00 AM – 5:30 AM night tariff window.",
            "Inspect thermal silicone gaskets on oven perimeter doors to recover an estimated 10% in radiated heat loss.",
            "Interlock exhaust ventilation hoods with variable speed drives (VFD) to eliminate constant 100% blower draw."
        ],
        "24/7 Cold Pharmacy": [
            "Isolate non-critical storefront showcase display lighting from critical vaccine cold storage circuits.",
            "Schedule automated defrost cycles on medical deep freezers strictly between 2:00 AM and 4:00 AM.",
            "Maintain 150mm clearance behind condenser coils to drop continuous compressor run-time by 15%."
        ]
    }

    action_plan = action_plans.get(subcategory, action_plans["Flour Mill"])

    compliance_badge = {
        "title": "ESG Tier 1 Clean Energy Vendor Status",
        "valid_through": "Q4 2026",
        "issuing_body": "Clean Energy Municipal Compliance Board"
    }

    return CommercialSavingsResponse(
        meter_id=meter_id,
        direct_opex_preserved_inr=direct_opex,
        operating_margin_boost_pct=operating_margin_boost,
        equivalent_revenue_inr=equivalent_revenue,
        tod_surcharges_avoided_inr=tod_avoided,
        monthly_baseline_inr=monthly_baseline,
        monthly_optimized_inr=monthly_optimized,
        cumulative_profit_inr=cumulative_profit,
        action_plan=action_plan,
        compliance_badge=compliance_badge
    )

def run_simulation(
    df: pd.DataFrame,
    profile: Dict[str, Any],
    target_reduction_pct: float = 15.0
) -> SimulationResult:
    """Calculates interactive what-if savings transparently with documented assumptions."""
    tariff_calc = calculate_tariff_bracket(df, profile)
    effective_rate = tariff_calc.average_effective_rate_inr
    
    unique_days = df["date"].nunique() if not df.empty else 30
    total_kwh = float(df["energy_kwh"].sum()) if not df.empty else (profile.get("base_daily_kwh", 18.0) * 30)
    daily_avg_kwh = total_kwh / max(1, unique_days)
    baseline_monthly_kwh = daily_avg_kwh * 30.0

    reduction_factor = target_reduction_pct / 100.0
    reduced_monthly_kwh = baseline_monthly_kwh * (1.0 - reduction_factor)
    kwh_saved_monthly = baseline_monthly_kwh * reduction_factor

    monthly_cash_saved = round(kwh_saved_monthly * effective_rate, 2)
    annual_cash_saved = round(monthly_cash_saved * 12.0, 2)

    # Carbon savings: CEA factor 0.72 kg CO2e / kWh
    co2_avoided_kg = round(kwh_saved_monthly * 0.72, 1)
    trees_offset = round(co2_avoided_kg / 1.67, 1)

    return SimulationResult(
        target_reduction_pct=target_reduction_pct,
        monthly_saved_inr=monthly_cash_saved,
        annual_saved_inr=annual_cash_saved,
        co2_avoided_kg_per_month=co2_avoided_kg,
        equivalent_trees_monthly=trees_offset,
        baseline_monthly_kwh=round(baseline_monthly_kwh, 1),
        reduced_monthly_kwh=round(reduced_monthly_kwh, 1),
        applicable_tariff_rate=round(effective_rate, 2)
    )

