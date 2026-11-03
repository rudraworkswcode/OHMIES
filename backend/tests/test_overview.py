import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_overview_requires_auth():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/overview")
        assert resp.status_code == 401

@pytest.mark.anyio
async def test_overview_metrics_tab1():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Login first
        login_resp = await client.post(
            "/api/auth/login",
            json={"user_id": "JEEVAN KRISHNA", "password": "JAI RNSIT"}
        )
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Fetch overview
        resp = await client.get("/api/overview", headers=headers)
        assert resp.status_code == 200
        data = resp.json()

        # Check User & Header information
        assert "user" in data
        assert data["user"]["display_name"] == "Jeevan Krishna"
        assert "goal_description" in data["user"]
        assert "goal_kwh_per_week" in data["user"]

        # 1. Average Daily Draw card
        daily_card = data["average_daily_draw"]
        assert "value" in daily_card
        assert daily_card["unit"] == "kWh/day"
        assert daily_card["value"] > 0
        assert "reporting_period" in daily_card

        # 2. Peak Window Intensity card
        peak_card = data["peak_window_intensity"]
        assert "energy_kwh" in peak_card
        assert "demand_kw" in peak_card
        assert "window" in peak_card
        assert peak_card["unit_energy"] == "kWh"
        assert peak_card["unit_demand"] == "kW"

        # 3. Grid Carbon Footprint card
        carbon_card = data["grid_carbon_footprint"]
        assert "daily_emissions_kg_co2e" in carbon_card
        assert carbon_card["emission_factor_kg_per_kwh"] == 0.72
        assert "CEA" in carbon_card["factor_source"]

        # 4. Tariff Bracket card
        tariff_card = data["tariff_bracket"]
        assert "tariff_category" in tariff_card
        assert "average_effective_rate_inr" in tariff_card
        assert "slab_structure" in tariff_card
        assert tariff_card["average_effective_rate_inr"] > 0

        # Intelligent Consumption Summary
        summary = data["summary"]
        assert "headline" in summary
        assert "current_consumption_kwh" in summary
        assert "daily_average_kwh" in summary
        assert "actionable_recommendations" in summary
        assert len(summary["actionable_recommendations"]) > 0
        assert "trend_direction" in summary

@pytest.mark.anyio
async def test_overview_profile_archetype_switch():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/auth/login",
            json={"user_id": "JEEVAN KRISHNA", "password": "JAI RNSIT"}
        )
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Query commercial bakery profile
        resp = await client.get("/api/overview?meter_id=COM-3390", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["user"]["sector"] == "Commercial"
        assert data["user"]["subcategory"] == "Commercial Bakery"
        assert data["tariff_bracket"]["average_effective_rate_inr"] > 10.0

