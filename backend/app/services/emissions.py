import pandas as pd
from app.core.config import settings
from app.schemas.overview_schemas import CarbonFootprintMetric

def calculate_grid_carbon_footprint(df: pd.DataFrame) -> CarbonFootprintMetric:
    """
    Estimates grid carbon emissions associated with electricity consumption.
    Emissions (kg CO2e) = Energy (kWh) * Emission Factor (kg CO2e/kWh)
    """
    emission_factor = settings.GRID_EMISSION_FACTOR_KG_PER_KWH
    factor_source = "Central Electricity Authority (CEA) India CO2 Baseline Database v19 (0.72 kg CO2e/kWh)"

    if df.empty or "energy_kwh" not in df.columns:
        return CarbonFootprintMetric(
            total_emissions_kg_co2e=0.0,
            daily_emissions_kg_co2e=0.0,
            emission_factor_kg_per_kwh=emission_factor,
            factor_source=factor_source,
            equivalent_trees_offset_per_month=0.0
        )

    unique_days = df["date"].nunique()
    total_kwh = float(df["energy_kwh"].sum())
    daily_avg_kwh = total_kwh / max(1, unique_days)

    total_emissions = total_kwh * emission_factor
    daily_emissions = daily_avg_kwh * emission_factor
    monthly_emissions = daily_emissions * 30.0

    # 1 mature tree absorbs ~20 kg CO2 per year (≈ 1.67 kg CO2 / month)
    equivalent_trees_monthly = monthly_emissions / 1.67

    return CarbonFootprintMetric(
        total_emissions_kg_co2e=round(total_emissions, 2),
        daily_emissions_kg_co2e=round(daily_emissions, 2),
        emission_factor_kg_per_kwh=emission_factor,
        factor_source=factor_source,
        equivalent_trees_offset_per_month=round(equivalent_trees_monthly, 1)
    )

