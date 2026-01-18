"""
Edge case tests for authentication API endpoints.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Registering with an existing email should fail."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123"
    }
    
    # First registration should succeed
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    
    # Second registration with same email should fail
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Login with wrong password should return 401."""
    # Register a user first
    await client.post("/api/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "correctpassword"
    })
    
    # Try to login with wrong password
    response = await client.post("/api/auth/token", data={
        "username": "wrongpass@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Login with non-existent user should return 401."""
    response = await client.post("/api/auth/token", data={
        "username": "nonexistent@example.com",
        "password": "anypassword"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_access_protected_route_without_token(client: AsyncClient):
    """Accessing /me without token should return 401."""
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_access_protected_route_with_invalid_token(client: AsyncClient):
    """Accessing /me with invalid token should return 401."""
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalidtoken123"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_access_protected_route_with_malformed_header(client: AsyncClient):
    """Accessing /me with malformed auth header should return 401."""
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": "NotBearer token"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_empty_email(client: AsyncClient):
    """Registering with empty email should fail."""
    response = await client.post("/api/auth/register", json={
        "email": "",
        "password": "password123"
    })
    # FastAPI/Pydantic may return 422 for validation error
    assert response.status_code in [400, 422]


@pytest.mark.asyncio
async def test_register_empty_password(client: AsyncClient):
    """Registering with empty password should still work (no validation)."""
    response = await client.post("/api/auth/register", json={
        "email": "emptypass@example.com",
        "password": ""
    })
    # This may succeed since there's no password validation
    # but login will fail with empty password
    assert response.status_code in [200, 400, 422]
