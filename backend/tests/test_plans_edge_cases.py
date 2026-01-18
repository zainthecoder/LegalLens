"""
Edge case tests for Plans API endpoints.
"""
import pytest
from httpx import AsyncClient
from bson import ObjectId


async def get_auth_token(client: AsyncClient, email: str, password: str) -> str:
    """Helper to register a user and get an auth token."""
    await client.post("/api/auth/register", json={
        "email": email,
        "password": password
    })
    response = await client.post("/api/auth/token", data={
        "username": email,
        "password": password
    })
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_list_plans_empty(client: AsyncClient):
    """New user should have empty plans list."""
    token = await get_auth_token(client, "newuser@example.com", "password123")
    
    response = await client.get(
        "/api/plans",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_nonexistent_plan(client: AsyncClient):
    """Getting a non-existent plan should return 404."""
    token = await get_auth_token(client, "nopplan@example.com", "password123")
    
    # Use a valid ObjectId format but one that doesn't exist
    fake_id = str(ObjectId())
    
    response = await client.get(
        f"/api/plans/{fake_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_plan(client: AsyncClient):
    """Deleting a non-existent plan should return 404."""
    token = await get_auth_token(client, "nodelete@example.com", "password123")
    
    fake_id = str(ObjectId())
    
    response = await client.delete(
        f"/api/plans/{fake_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_access_other_user_plan(client: AsyncClient):
    """User should not be able to access another user's plan."""
    # Create first user and a plan
    token1 = await get_auth_token(client, "user1@example.com", "password123")
    
    # Create a plan by sending a chat message
    async with client.stream(
        "POST",
        "/api/chat",
        json={"messages": [{"role": "user", "content": "Create a simple plan"}]},
        headers={"Authorization": f"Bearer {token1}"}
    ) as response:
        async for _ in response.aiter_text():
            pass
    
    # Get user1's plan
    plans_response = await client.get(
        "/api/plans",
        headers={"Authorization": f"Bearer {token1}"}
    )
    user1_plan_id = plans_response.json()[0]["_id"]
    
    # Create second user
    token2 = await get_auth_token(client, "user2@example.com", "password123")
    
    # User2 tries to access User1's plan - should return 404 (not 403 to avoid leaking existence)
    response = await client.get(
        f"/api/plans/{user1_plan_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_other_user_plan(client: AsyncClient):
    """User should not be able to delete another user's plan."""
    # Create first user and a plan
    token1 = await get_auth_token(client, "owner@example.com", "password123")
    
    async with client.stream(
        "POST",
        "/api/chat",
        json={"messages": [{"role": "user", "content": "Create my plan"}]},
        headers={"Authorization": f"Bearer {token1}"}
    ) as response:
        async for _ in response.aiter_text():
            pass
    
    plans_response = await client.get(
        "/api/plans",
        headers={"Authorization": f"Bearer {token1}"}
    )
    plan_id = plans_response.json()[0]["_id"]
    
    # Create second user
    token2 = await get_auth_token(client, "attacker@example.com", "password123")
    
    # User2 tries to delete User1's plan
    response = await client.delete(
        f"/api/plans/{plan_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_chat_with_invalid_plan_id(client: AsyncClient):
    """Chatting with an invalid plan_id should return 404."""
    token = await get_auth_token(client, "badplan@example.com", "password123")
    
    fake_id = str(ObjectId())
    
    async with client.stream(
        "POST",
        "/api/chat",
        json={
            "messages": [{"role": "user", "content": "Continue this plan"}],
            "plan_id": fake_id
        },
        headers={"Authorization": f"Bearer {token}"}
    ) as response:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_plans_require_authentication(client: AsyncClient):
    """Plans endpoints should require authentication."""
    # List plans
    response = await client.get("/api/plans")
    assert response.status_code == 401
    
    # Get specific plan
    response = await client.get(f"/api/plans/{ObjectId()}")
    assert response.status_code == 401
    
    # Delete plan
    response = await client.delete(f"/api/plans/{ObjectId()}")
    assert response.status_code == 401
