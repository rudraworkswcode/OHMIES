import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from app.schemas.overview_schemas import MetricValue, PeakIntensityMetric

def calculate_average_daily_draw(df: pd.DataFrame) -> MetricValue:
    """
    Calculates average daily energy consumption in kWh/day.
    Total kWh divided by number of unique days.
    """
    if df.empty or "energy_kwh" not in df.columns:
        return MetricValue(value=0.0, unit="kWh/day", reporting_period="N/A", subtext="No data recorded")
        
    unique_days = df["date"].nunique()
    total_kwh = df["energy_kwh"].sum()
    avg_daily = total_kwh / max(1, unique_days)
    
    start_date = df["date"].min()
    end_date = df["date"].max()
    reporting_period = f"{start_date} to {end_date} ({unique_days} days)"
    
    return MetricValue(
        value=round(float(avg_daily), 2),
        unit="kWh/day",
        reporting_period=reporting_period,
        subtext=f"Total: {round(float(total_kwh), 1)} kWh across {unique_days} days"
    )

def calculate_peak_window_intensity(df: pd.DataFrame) -> PeakIntensityMetric:
    """
    Identifies the highest 4-hour electricity consumption window.
    Distinguishes cumulative energy (kWh) from peak power/demand (kW).
    """
    if df.empty or "hour" not in df.columns:
        return PeakIntensityMetric(
            energy_kwh=0.0,
            demand_kw=0.0,
            window="N/A",
            peak_hour="N/A"
        )
        
    # Group by hour of day (0-23) to compute average hourly energy and peak demand
    hourly_agg = df.groupby("hour").agg({
        "energy_kwh": "mean",
        "demand_kw": "max"
    }).reset_index()

    # Find maximum 4-hour contiguous window
    n = len(hourly_agg)
    max_energy_sum = -1.0
    best_start_hour = 0
    best_peak_demand = 0.0

    # Test rolling 4-hour blocks
    for start in range(n):
        window_hours = [(start + i) % 24 for i in range(4)]
        window_rows = hourly_agg[hourly_agg["hour"].isin(window_hours)]
        energy_sum = window_rows["energy_kwh"].sum()
        peak_demand = window_rows["demand_kw"].max()
        
        if energy_sum > max_energy_sum:
            max_energy_sum = energy_sum
            best_start_hour = start
            best_peak_demand = peak_demand

    end_hour = (best_start_hour + 4) % 24
    
    start_str = f"{best_start_hour:02d}:00"
    end_str = f"{end_hour:02d}:00"
    window_label = f"{start_str} - {end_str}"
    
    peak_single_hour = int(hourly_agg.loc[hourly_agg["energy_kwh"].idxmax()]["hour"])
    peak_single_hour_str = f"{peak_single_hour:02d}:00"

    return PeakIntensityMetric(
        energy_kwh=round(float(max_energy_sum), 2),
        demand_kw=round(float(best_peak_demand), 2),
        window=window_label,
        peak_hour=peak_single_hour_str
    )

def calculate_consumption_trend(df: pd.DataFrame) -> Tuple[str, float]:
    """
    Compares the older half of the reporting period to the recent half
    to determine consumption trajectory.
    Returns (direction, percentage).
    """
    if df.empty or df["date"].nunique() < 2:
        return "steady", 0.0

    daily = df.groupby("date")["energy_kwh"].sum().reset_index()
    mid = len(daily) // 2
    first_half = daily.iloc[:mid]["energy_kwh"].mean()
    second_half = daily.iloc[mid:]["energy_kwh"].mean()

    if first_half <= 0:
        return "steady", 0.0

    diff_pct = ((second_half - first_half) / first_half) * 100.0

    if diff_pct > 2.5:
        return "increasing", round(abs(diff_pct), 1)
    elif diff_pct < -2.5:
        return "decreasing", round(abs(diff_pct), 1)
    else:
        return "steady", round(abs(diff_pct), 1)

