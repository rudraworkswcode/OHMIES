import pandas as pd
import pytest
from app.services.consumption import (
    calculate_average_daily_draw,
    calculate_peak_window_intensity,
    calculate_consumption_trend
)
from app.services.emissions import calculate_grid_carbon_footprint
from app.services.tariffs import calculate_tariff_bracket
from app.db.seed_data import generate_hourly_records, PROFILES

def test_daily_draw_calculation():
    df = generate_hourly_records("DOM-9821", days=30)
    metric = calculate_average_daily_draw(df)
    assert metric.value > 15.0 and metric.value < 22.0
    assert metric.unit == "kWh/day"
    assert "30 days" in metric.reporting_period

def test_peak_window_distinction():
    df = generate_hourly_records("DOM-9821", days=30)
    peak = calculate_peak_window_intensity(df)
    # Ensure kWh energy and kW demand are both computed and non-zero
    assert peak.energy_kwh > 0
    assert peak.demand_kw > 0
    assert peak.unit_energy == "kWh"
    assert peak.unit_demand == "kW"
    assert "-" in peak.window

def test_grid_carbon_calculation():
    df = generate_hourly_records("DOM-9821", days=30)
    carbon = calculate_grid_carbon_footprint(df)
    expected_emissions = round(float(df["energy_kwh"].sum()) * 0.72, 2)
    assert abs(carbon.total_emissions_kg_co2e - expected_emissions) < 0.1
    assert carbon.emission_factor_kg_per_kwh == 0.72

def test_telescopic_tariff_calculation():
    profile = PROFILES["DOM-9821"]
    df = generate_hourly_records("DOM-9821", days=30)
    tariff = calculate_tariff_bracket(df, profile)
    assert tariff.average_effective_rate_inr >= 6.0
    assert "Telescopic" in tariff.slab_structure

