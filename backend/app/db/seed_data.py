import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List

# Classification catalogues from PRD & sample.md
SECTOR_DOMESTIC = "Domestic"
SECTOR_COMMERCIAL = "Commercial"

DOMESTIC_SUBCATEGORIES = [
    "High-Rise Apartments",
    "Independent Bungalows",
    "Compact Studio or Shared Accommodation"
]

COMMERCIAL_SUBCATEGORIES = {
    "MICRO": ["Flour Mill", "Garment and Tailor", "Salon and Wellness"],
    "SMALL": ["Auto Garage", "Photo Studio", "Commercial Bakery"],
    "MEDIUM": ["IT / Co-working Space", "Retail Showroom", "24/7 Cold Pharmacy"]
}

# Profile configurations with baseline attributes
PROFILES: Dict[str, Dict[str, Any]] = {
    "DOM-9821": {
        "user_id": "Jeevan",
        "display_name": "Jeevan Krishna",
        "meter_id": "DOM-9821",
        "sector": SECTOR_DOMESTIC,
        "subcategory": "High-Rise Apartments",
        "goal_kwh_per_week": 14.5,
        "goal_description": "Cut 14.5 kWh this week (Save ~₹165)",
        "base_daily_kwh": 18.4,
        "peak_window_hours": (19, 23),  # 7:00 PM to 11:30 PM
        "tariff_category": "Domestic LT-2(a) Telescopic Slab",
        "tariff_base_rate": 8.50,
        "fixed_charge": 120.0
    },
    "DOM-1044": {
        "user_id": "Bungalow_User",
        "display_name": "Arjun Sharma",
        "meter_id": "DOM-1044",
        "sector": SECTOR_DOMESTIC,
        "subcategory": "Independent Bungalows",
        "goal_kwh_per_week": 22.0,
        "goal_description": "Cut 22.0 kWh this week (Save ~₹240)",
        "base_daily_kwh": 26.2,
        "peak_window_hours": (11, 17),  # Daytime peak HVAC
        "tariff_category": "Domestic LT-2(a) High Slab",
        "tariff_base_rate": 9.20,
        "fixed_charge": 180.0
    },
    "DOM-3012": {
        "user_id": "Studio_User",
        "display_name": "Rhea Pillai",
        "meter_id": "DOM-3012",
        "sector": SECTOR_DOMESTIC,
        "subcategory": "Compact Studio or Shared Accommodation",
        "goal_kwh_per_week": 8.0,
        "goal_description": "Cut 8.0 kWh this week (Save ~₹90)",
        "base_daily_kwh": 9.5,
        "peak_window_hours": (20, 24),
        "tariff_category": "Domestic LT-2(a) Low Slab",
        "tariff_base_rate": 6.80,
        "fixed_charge": 80.0
    },
    "COM-7714": {
        "user_id": "Flour_Mill_Operator",
        "display_name": "Mahadev Flour Mills",
        "meter_id": "COM-7714",
        "sector": SECTOR_COMMERCIAL,
        "business_size": "MICRO",
        "subcategory": "Flour Mill",
        "goal_kwh_per_week": 45.0,
        "goal_description": "Cut 45.0 kWh this week (Save ~₹520)",
        "base_daily_kwh": 54.0,
        "peak_window_hours": (7, 13),  # Morning grinding shift
        "tariff_category": "Commercial LT-5(a) Micro-Industry ToD",
        "tariff_base_rate": 10.50,
        "fixed_charge": 350.0
    },
    "COM-3390": {
        "user_id": "Bakery_Manager",
        "display_name": "OvenFresh Artisanal Bakery",
        "meter_id": "COM-3390",
        "sector": SECTOR_COMMERCIAL,
        "business_size": "SMALL",
        "subcategory": "Commercial Bakery",
        "goal_kwh_per_week": 70.0,
        "goal_description": "Cut 70.0 kWh this week (Save ~₹850)",
        "base_daily_kwh": 88.0,
        "peak_window_hours": (3, 9),  # Early morning baking cycle
        "tariff_category": "Commercial LT-5(b) Small Enterprise ToD",
        "tariff_base_rate": 11.20,
        "fixed_charge": 650.0
    },
    "MED-4501": {
        "user_id": "Pharmacy_Cold_Chain",
        "display_name": "Apex 24/7 Cold Chain Pharmacy",
        "meter_id": "MED-4501",
        "sector": SECTOR_COMMERCIAL,
        "business_size": "MEDIUM",
        "subcategory": "24/7 Cold Pharmacy",
        "goal_kwh_per_week": 90.0,
        "goal_description": "Cut 90.0 kWh this week (Save ~₹1,150)",
        "base_daily_kwh": 124.0,
        "peak_window_hours": (0, 24),  # 24/7 continuous refrigeration
        "tariff_category": "Commercial HT-2(b) Continuous Cold Chain",
        "tariff_base_rate": 11.80,
        "fixed_charge": 1200.0
    }
}

def generate_hourly_records(meter_id: str, days: int = 30) -> pd.DataFrame:
    """
    Generates deterministic, realistic 30-day hourly consumption records
    traceable to the specific sector and archetype profile.
    """
    profile = PROFILES.get(meter_id, PROFILES["DOM-9821"])
    base_daily = profile["base_daily_kwh"]
    base_hourly = base_daily / 24.0
    peak_start, peak_end = profile["peak_window_hours"]

    # Fixed seed for deterministic, repeatable testing
    np.random.seed(42 + hash(meter_id) % 1000)
    
    end_time = datetime(2026, 11, 1, 23, 0, tzinfo=timezone(timedelta(hours=5, minutes=30)))
    timestamps = [end_time - timedelta(hours=i) for i in range(days * 24)]
    timestamps.reverse()

    records: List[Dict[str, Any]] = []
    for ts in timestamps:
        hour = ts.hour
        is_weekend = ts.weekday() >= 5
        
        # Calculate hourly consumption multiplier based on archetype profile
        if peak_start <= hour <= peak_end or (peak_start > peak_end and (hour >= peak_start or hour <= peak_end)):
            multiplier = 1.85 if not is_weekend else 2.10
        elif 1 <= hour <= 5:
            multiplier = 0.42 if profile["subcategory"] != "24/7 Cold Pharmacy" else 0.95
        else:
            multiplier = 0.85
            
        noise = np.random.normal(0, 0.05 * base_hourly)
        energy_kwh = max(0.05, round((base_hourly * multiplier) + noise, 3))
        # Instantaneous power/demand in kW (with slight load factor variation)
        demand_kw = round(energy_kwh * (1.15 + np.random.uniform(0.05, 0.25)), 2)
        power_factor = round(0.92 + np.random.uniform(-0.04, 0.06), 2)
        power_factor = min(1.0, max(0.80, power_factor))

        records.append({
            "timestamp": ts.isoformat(),
            "date": ts.strftime("%Y-%m-%d"),
            "hour": hour,
            "meter_id": meter_id,
            "sector": profile["sector"],
            "subcategory": profile["subcategory"],
            "energy_kwh": energy_kwh,
            "demand_kw": demand_kw,
            "power_factor": power_factor
        })

    df = pd.DataFrame(records)
    return df

