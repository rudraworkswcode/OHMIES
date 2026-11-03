import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_analytics_consumption_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Authenticate
        login_resp = await client.post(
            "/api/auth/login",
            json={"user_id": "JEEVAN KRISHNA", "password": "JAI RNSIT"}
        )
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Query analytics 30d
        resp = await client.get("/api/analytics/consumption?range=30d", headers=headers)
        assert resp.status_code == 200
        data = resp.json()

        # Check daily trends
        assert "daily_trends" in data
        assert len(data["daily_trends"]) == 30
        first_day = data["daily_trends"][0]
        assert "energy_kwh" in first_day
        assert "rolling_avg_kwh" in first_day

        # Check weekly data (consistent 7-day bins)
        assert "weekly_data" in data
        assert len(data["weekly_data"]) == 4
        assert data["weekly_data"][0]["week_label"] == "Week 1"
        assert data["weekly_data"][0]["total_kwh"] > 0

        # Check category pie slices
        assert "equipment_breakdown" in data
        assert len(data["equipment_breakdown"]) > 0
        assert sum(s["percentage"] for s in data["equipment_breakdown"]) > 95.0

        # Check time slot slices
        assert "time_slot_breakdown" in data
        assert len(data["time_slot_breakdown"]) == 4

        # Check smart tips
        assert "smart_tips" in data
        assert len(data["smart_tips"]) > 0

@pytest.mark.anyio
async def test_analytics_range_filter():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/auth/login",
            json={"user_id": "JEEVAN KRISHNA", "password": "JAI RNSIT"}
        )
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp_7d = await client.get("/api/analytics/consumption?range=7d", headers=headers)
        assert resp_7d.status_code == 200
        assert len(resp_7d.json()["daily_trends"]) == 7

