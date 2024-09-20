import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture(scope="session")
async def auth_token(ac: AsyncClient):
    user_data1 = {
        "email": "testuser@example.com",
        "password": "testpassword",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    }
    user_data2 = {
        "username": "testuser@example.com",
        "password": "testpassword",
    }

    r1 = await ac.post("/auth/register", json=user_data1)
    assert r1.status_code == 201

    r2 = await ac.post("/auth/jwt/login", data=user_data2)
    assert r2.status_code == 200

    token = r2.json().get("access_token")
    assert token is not None
    return token


@pytest_asyncio.fixture(scope="session")
async def get_header(ac: AsyncClient, auth_token: str):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.mark.asyncio
async def test_successful_add(ac: AsyncClient, get_header: dict):
    data = {
        "text": "text"
    }
    r = await ac.post("/notes", headers=get_header, params=data)
    assert r.status_code == 201


@pytest.mark.asyncio
async def test_successful_added_corrected_and_got(ac: AsyncClient, get_header: dict):
    data = {
        "text": "купитб маме малоко"
    }
    r1 = await ac.post("/notes", headers=get_header, params=data)
    assert r1.status_code == 201
    assert r1.json().get("note_id")
    r2 = await ac.get("/notes", headers=get_header)
    assert r2.status_code == 200
    assert r2.json()[0].get("text") == "купить маме молоко"