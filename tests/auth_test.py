import pytest

@pytest.mark.asyncio
async def test_login(client):
    res = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "test1234"
    })
    assert res.status_code == 200
    assert res.json()["ok"] is True
    assert "access_token" in res.json()["data"]

@pytest.mark.asyncio
async def test_me(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    me_res = await client.get("/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["ok"] is True