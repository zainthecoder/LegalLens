
import pytest
from httpx import AsyncClient

# --- Auth Tests ---

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    # First ensure user exists (if running independently, but flow implies register first)
    # We rely on order or previous test, but better to be isolated or re-register.
    # Beanie test DB persists across session due to scope="session" fixture, so user from test_register_user exists.
    
    response = await client.post("/api/auth/token", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    # Login to get token
    token = await test_login_user(client)
    
    response = await client.get("/api/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

# --- Plan Tests ---

@pytest.mark.asyncio
async def test_create_plan_implicitly_via_chat(client: AsyncClient):
    token = await test_login_user(client)
    
    # Send a chat message which should create a plan
    # Note: /api/chat is a streaming endpoint. Testing it with httpx requires handling stream or simple request.
    # httpx.post return response object, we can check basic status.
    # However, the endpoint returns StreamingResponse.
    
    # We need to simulate a chat request
    payload = {
        "messages": [{"role": "user", "content": "Create a plan for a NDA"}]
    }
    
    async with client.stream("POST", "/api/chat", json=payload, headers={"Authorization": f"Bearer {token}"}) as response:
        assert response.status_code == 200
        # We can consume stream if needed, but for now just checking connection and status
        async for chunk in response.aiter_text():
            pass

    # Now check if plan was created
    # We need to hit GET /plans endpoint
    response = await client.get("/api/plans", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    plans = response.json()
    assert len(plans) > 0
    # Store plan_id for next tests
    return plans[0]["_id"], token

@pytest.mark.asyncio
async def test_get_plan_details(client: AsyncClient):
    plan_id, token = await test_create_plan_implicitly_via_chat(client)
    
    response = await client.get(f"/api/plans/{plan_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "plan" in data
    assert "chat_history" in data
    assert data["plan"]["_id"] == plan_id

@pytest.mark.asyncio
async def test_delete_plan(client: AsyncClient):
    plan_id, token = await test_create_plan_implicitly_via_chat(client)
    
    response = await client.delete(f"/api/plans/{plan_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Plan deleted successfully"
    
    # Verify deletion
    response = await client.get(f"/api/plans/{plan_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
