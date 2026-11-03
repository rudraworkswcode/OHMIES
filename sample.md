# OHMies — Sample Data and Dataset Guide

## 1. Purpose

This document defines the classification system, illustrative data structures, and data-handling rules for OHMies.

The actual electricity datasets are stored in Supabase and will be supplied separately.

**IMPORTANT:** The coding agent must inspect the actual datasets before implementing database queries.

Do not assume the illustrative structures in this document match the existing database.

---

## 2. Electricity Sector Classification

### A. Domestic Household

| Sector | Subcategory |
|---|---|
| Domestic | High-Rise Apartments |
| Domestic | Independent Bungalows |
| Domestic | Compact Studio or Shared Accommodation |

### B. Commercial / Industrial

| Business Size | Business Type |
|---|---|
| MICRO | Flour Mill |
| MICRO | Garment and Tailor |
| MICRO | Salon and Wellness |
| SMALL | Auto Garage |
| SMALL | Photo Studio |
| SMALL | Commercial Bakery |
| MEDIUM | IT / Co-working Space |
| MEDIUM | Retail Showroom |
| MEDIUM | 24/7 Cold Pharmacy |

These categories must be configurable.

---

## 3. Illustrative Data Structures

The following examples are only proposed logical structures.

### A. User Profile

```json
{
  "user_id": "example-user-id",
  "display_name": "Jeevan",
  "sector": "Domestic",
  "subcategory": "High-Rise Apartments",
  "goal_kwh_per_month": null
}
```

### B. Electricity Consumption Record

```json
{
  "record_id": "example-record-id",
  "account_id": "example-user-id",
  "recorded_at": "2026-11-01T10:00:00+05:30",
  "energy_kwh": 1.25,
  "source": "demo"
}
```

### C. Tariff Information

```json
{
  "tariff_id": "example-tariff-id",
  "label": "Illustrative tariff",
  "rate_inr_per_kwh": null,
  "effective_from": null,
  "effective_to": null
}
```

### D. Carbon Emissions Factor

```json
{
  "region": "India",
  "factor_value": null,
  "factor_unit": "kg CO2e/kWh",
  "effective_date": null
}
```

Null values are intentional.

Do not invent electricity tariff rates or carbon emission factors.

---

## 4. Dataset Inspection Requirements

Before connecting the dashboard to Supabase, inspect:

1. Existing table names.
2. Column names.
3. Data types.
4. Primary keys.
5. Foreign keys.
6. User/account relationships.
7. Timestamp format.
8. Timezone.
9. Electricity consumption units.
10. Sampling intervals.
11. Missing values.
12. Duplicate records.
13. Available tariff information.
14. Available carbon emission information.
15. Existing RLS policies.

Document the actual schema before writing the final database integration.

---

## 5. Metric Requirements

| Metric | Required Data |
|---|---|
| Average Daily Draw | Daily or timestamped energy consumption |
| Peak Window Intensity | Timestamped consumption or demand |
| Grid Carbon Footprint | Energy consumption and emission factor |
| Tariff Bracket | Applicable tariff configuration |
| Weekly Bar Graph | Timestamped consumption |
| Pie Chart | Consumption category breakdown |
| Savings | Consumption baseline and applicable tariff |

### Calculation rules

**Average Daily Draw**

Total energy consumption divided by the number of covered days.

**Peak Window Intensity**

Identify the highest-use period and calculate its consumption or demand.

**Grid Carbon Footprint**

Energy consumption × applicable emissions factor.

**Savings**

Compare baseline electricity costs against estimated costs after the proposed reduction.

All calculations must use compatible units and documented assumptions.

---

## 6. Demo Data Policy

Demo data may be used during development.

However:

- Clearly label demo data.
- Never mix demo and production records silently.
- Do not display demo statistics as actual user consumption.
- Keep demo fixtures separate from production datasets.
- Use deterministic demo records for repeatable testing.

If Supabase is unavailable, display a suitable connection or data-loading error instead of silently displaying fabricated values.

---

## 7. Development Test Identity

Example UID:

`Jeevan`

The example password supplied by the user must be configured locally through a secure environment variable or Supabase Auth.

Never:
- Hardcode it in React.
- Commit it to Git.
- Store it in a public JSON file.
- Include it in application logs.

---

## 8. Smart Tips Catalogue

Smart Tips will initially be predefined and hardcoded.

They should be selected based on the user's sector and subcategory.

### Domestic Household

**Tip 1:** Switch off lights and fans in unoccupied rooms.

**Tip 2:** Use natural daylight wherever practical.

**Tip 3:** Maintain air-conditioning filters and avoid unnecessarily low temperature settings.

### MICRO Businesses

**Flour Mill**
- Inspect motor condition.
- Avoid unnecessary idle-running.
- Check belt tension and equipment maintenance.

**Garment and Tailor**
- Switch off irons and equipment during breaks.
- Avoid leaving high-load equipment unnecessarily powered on.

**Salon and Wellness**
- Switch off water heaters when not required.
- Manage lighting and equipment operating hours.

### SMALL Businesses

**Auto Garage**
- Switch off unused compressors and equipment.
- Use task lighting where practical.

**Photo Studio**
- Turn off studio lights and computers when not required.

**Commercial Bakery**
- Optimise oven preheating.
- Avoid unnecessary heat loss.
- Organise baking schedules efficiently.

### MEDIUM Businesses

**IT / Co-working Space**
- Enable power-saving settings.
- Optimise cooling schedules.
- Switch off unused workstations.

**Retail Showroom**
- Use efficient lighting.
- Manage display lighting outside operating hours.

**24/7 Cold Pharmacy**
- Maintain refrigerator door seals.
- Ensure proper ventilation around refrigeration equipment.
- Follow required medicine-storage temperature guidelines.

These are general recommendations, not guaranteed savings. Never recommend actions that compromise safety, equipment requirements, or pharmaceutical storage conditions.

---

## 9. Data Quality Rules

- Validate numerical consumption values.
- Check units before calculations.
- Handle missing timestamps.
- Identify duplicate records.
- Use consistent timezones.
- Handle incomplete weeks correctly.
- Do not invent missing values.
- Do not compare different reporting periods without explaining the method.
- Clearly identify estimates and assumptions.

The data displayed on OHMies must be trustworthy and traceable to its source.