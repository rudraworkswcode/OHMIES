import pandas as pd
from typing import Dict, Any
from app.schemas.overview_schemas import TariffBracketMetric

def calculate_tariff_bracket(df: pd.DataFrame, profile: Dict[str, Any]) -> TariffBracketMetric:
    """
    Computes effective electricity tariff based on sector, telescopic slabs,
    and fixed charges without assuming a flat tariff rate.
    """
    sector = profile.get("sector", "Domestic")
    subcategory = profile.get("subcategory", "High-Rise Apartments")
    category_name = profile.get("tariff_category", "Domestic LT-2(a) Telescopic Slab")
    fixed_charge = float(profile.get("fixed_charge", 120.0))

    if df.empty or "energy_kwh" not in df.columns:
        return TariffBracketMetric(
            tariff_category=category_name,
            average_effective_rate_inr=8.50,
            slab_structure="Standard Slabs",
            fixed_charge_inr=fixed_charge,
            estimated_daily_cost_inr=0.0
        )

    unique_days = df["date"].nunique()
    total_kwh = float(df["energy_kwh"].sum())
    daily_avg_kwh = total_kwh / max(1, unique_days)
    monthly_estimated_kwh = daily_avg_kwh * 30.0

    if sector == "Domestic":
        # Telescopic 3-tier slab computation:
        # Tier 1: 0 to 100 kWh @ Rs. 4.75
        # Tier 2: 101 to 200 kWh @ Rs. 7.00
        # Tier 3: Above 200 kWh @ Rs. 8.50
        tier1_kwh = min(100.0, monthly_estimated_kwh)
        tier2_kwh = max(0.0, min(100.0, monthly_estimated_kwh - 100.0))
        tier3_kwh = max(0.0, monthly_estimated_kwh - 200.0)

        tier1_cost = tier1_kwh * 4.75
        tier2_cost = tier2_kwh * 7.00
        tier3_cost = tier3_kwh * 8.50
        
        monthly_variable_cost = tier1_cost + tier2_cost + tier3_cost
        monthly_total_cost = monthly_variable_cost + fixed_charge
        
        effective_rate = monthly_total_cost / max(1.0, monthly_estimated_kwh)
        daily_cost = monthly_total_cost / 30.0
        slab_desc = "Telescopic Slabs (₹4.75/₹7.00/₹8.50 per kWh) + ₹120 Fixed/mo"

    else:
        # Commercial Time-of-Day (ToD) tariff structure
        base_rate = float(profile.get("tariff_base_rate", 10.50))
        
        # Calculate time-of-day weighted consumption
        peak_kwh = df[df["hour"].between(18, 22)]["energy_kwh"].sum()
        off_peak_kwh = df[df["hour"].between(23, 23) | df["hour"].between(0, 6)]["energy_kwh"].sum()
        normal_kwh = total_kwh - (peak_kwh + off_peak_kwh)

        peak_surcharge = 1.50
        off_peak_rebate = 1.00

        total_variable_cost = (
            normal_kwh * base_rate +
            peak_kwh * (base_rate + peak_surcharge) +
            off_peak_kwh * (base_rate - off_peak_rebate)
        )
        
        pro_rated_fixed = (fixed_charge / 30.0) * unique_days
        total_billed = total_variable_cost + pro_rated_fixed
        effective_rate = total_billed / max(1.0, total_kwh)
        daily_cost = total_billed / max(1, unique_days)
        slab_desc = f"Commercial ToD: Base ₹{base_rate:.2f} (+₹1.50 Peak / -₹1.00 Off-Peak) + ₹{fixed_charge:.0f} Demand"

    return TariffBracketMetric(
        tariff_category=category_name,
        average_effective_rate_inr=round(float(effective_rate), 2),
        slab_structure=slab_desc,
        fixed_charge_inr=fixed_charge,
        estimated_daily_cost_inr=round(float(daily_cost), 2)
    )

