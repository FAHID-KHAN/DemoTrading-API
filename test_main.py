import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users/", json={"name": "Alice", "email": "alice@example.com", "balance": 1000.0})
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"

@pytest.mark.asyncio
async def test_get_balance():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_id = "test-id"  # Replace this with a valid user ID
        response = await ac.get(f"/users/{user_id}/balance/")
    assert response.status_code == 200
    assert "balance" in response.json()

@pytest.mark.asyncio
async def test_buy_asset():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/transactions/", json={
            "account_id": "test-id",  # Replace this with a valid user ID
            "asset": "AAPL",
            "quantity": 10,
            "price_per_unit": 150.0,
            "transaction_type": "buy"
        })
    assert response.status_code == 200
