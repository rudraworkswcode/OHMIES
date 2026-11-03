import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_invalid_login_credentials():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test wrong password
        resp = await client.post(
            "/api/auth/login",
            json={"user_id": "JEEVAN KRISHNA", "password": "WRONG_PASSWORD"}
        )
        assert resp.status_code == 401
        data = resp.json()
        assert data["detail"] == "Invalid UID and Password, pls try again later"

        # Test non-existent user
        resp2 = await client.post(
            "/api/auth/login",
            json={"user_id": "RandomUser", "password": "AnyPassword"}
        )
        assert resp2.status_code == 401
        data2 = resp2.json()
        assert data2["detail"] == "Invalid UID and Password, pls try again later"

@pytest.mark.anyio
async def test_valid_login_and_protected_me():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Valid login with JEEVAN KRISHNA
        resp = await client.post(
            "/api/auth/login",
            json={"user_id": "JEEVAN KRISHNA", "password": "JAI RNSIT"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["display_name"] == "Jeevan Krishna"
        assert data["sector"] == "Domestic"
        token = data["access_token"]

        # Access protected /api/auth/me
        headers = {"Authorization": f"Bearer {token}"}
        me_resp = await client.get("/api/auth/me", headers=headers)
        assert me_resp.status_code == 200
        me_data = me_resp.json()
        assert me_data["user_id"] == "Jeevan"
        assert me_data["meter_id"] == "DOM-9821"

@pytest.mark.anyio
async def test_unauthenticated_access_rejected():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/auth/me")
        assert resp.status_code == 401

