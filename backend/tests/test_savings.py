import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_domestic_greenpass_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/auth/login",
            json={"user_id": "JEEVAN KRISHNA", "password": "JAI RNSIT"}
        )
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp = await client.get("/api/savings/domestic", headers=headers)
        assert resp.status_code == 200
        data = resp.json()

        assert "roadmap" in data
        assert len(data["roadmap"]) == 7
        assert data["roadmap"][0]["cost_inr"] == 180.0
        assert "accumulated_savings_inr" in data
        assert data["streak_weeks"] >= 1
        assert "upcoming_milestone" in data

@pytest.mark.anyio
async def test_commercial_financials_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/auth/login",
            json={"user_id": "JEEVAN KRISHNA", "password": "JAI RNSIT"}
        )
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp = await client.get("/api/savings/commercial?meter_id=COM-7714", headers=headers)
        assert resp.status_code == 200
        data = resp.json()

        assert "direct_opex_preserved_inr" in data
        assert data["direct_opex_preserved_inr"] > 0
        assert data["operating_margin_boost_pct"] > 0
        assert "action_plan" in data
        assert len(data["action_plan"]) > 0

@pytest.mark.anyio
async def test_simulator_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/auth/login",
            json={"user_id": "JEEVAN KRISHNA", "password": "JAI RNSIT"}
        )
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp = await client.get("/api/savings/simulate?reduction_pct=20", headers=headers)
        assert resp.status_code == 200
        data = resp.json()

        assert data["target_reduction_pct"] == 20.0
        assert data["monthly_saved_inr"] > 0
        assert data["annual_saved_inr"] == round(data["monthly_saved_inr"] * 12.0, 2)
        assert data["co2_avoided_kg_per_month"] > 0
        assert data["equivalent_trees_monthly"] > 0

