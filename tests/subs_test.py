import pytest

@pytest.mark.asyncio
async def test_create_and_delete_subscription(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    subscription_data = {
        "plan_id": 22,
    }
    res = await client.post("/subscriptions/", json=subscription_data, headers=headers)

    if res.status_code != 200:
        print("Test Create Subscription Failed")
        print("Response Status Code:", res.status_code)
        print("Response JSON:", res.json())

    assert res.status_code == 200
    assert res.json()["ok"] is True

    cancel_res = await client.delete("/subscriptions/", headers=headers)

    if cancel_res.status_code != 200:
        print("Test Delete Subscription Failed")
        print("Response Status Code:", cancel_res.status_code)
        print("Response JSON:", cancel_res.json())

    print("Delete Subscription Response:", cancel_res.json())
    assert cancel_res.status_code == 200
    assert cancel_res.json()["ok"] is True


@pytest.mark.asyncio
async def test_get_user_subscription(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_id = 16
    res = await client.get(f"/subscriptions/{user_id}", headers=headers)

    if res.status_code != 200:
        print("Test Get User Subscription Failed")
        print("Response Status Code:", res.status_code)
        print("Response JSON:", res.json())

    assert res.status_code == 200
    assert res.json()["ok"] is True
    assert res.json()["data"]["user_id"] == user_id


@pytest.mark.asyncio
async def test_get_active_subscriptions(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = await client.get("/subscriptions/active", headers=headers)

    if res.status_code != 200:
        print("Test Get Active Subscriptions Failed")
        print("Response Status Code:", res.status_code)
        print("Response JSON:", res.json())

    assert res.status_code == 200
    assert res.json()["ok"] is True
    assert isinstance(res.json()["data"], list)



@pytest.mark.asyncio
async def test_get_user_subscription_history(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    user_id = 14
    res = await client.get(f"/subscriptions/history/{user_id}", headers=headers)

    if res.status_code != 200:
        print("Test Get User Subscription History Failed")
        print("Response Status Code:", res.status_code)
        print("Response JSON:", res.json())

    assert res.status_code == 200
    assert res.json()["ok"] is True
    assert isinstance(res.json()["data"], list)

