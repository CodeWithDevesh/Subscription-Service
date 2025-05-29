import pytest


@pytest.mark.asyncio
async def test_create_plan(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    plan_data = {
        "name": "Test Plan",
        "price": 99,
        "duration_days": 30,
        "features": ["feature1", "feature2"],
    }
    res = await client.post("/plans/", json=plan_data, headers=headers)

    # Debugging: Print the response if the test fails
    if res.status_code != 200:
        print("Test Create Plan Failed")
        print("Response Status Code:", res.status_code)
        print("Response JSON:", res.json())

    assert res.status_code == 200
    assert res.json()["ok"] is True
    assert res.json()["data"]["name"] == "Test Plan"

    # Clean up: Delete the created plan
    plan_id = res.json()["data"]["id"]
    del_res = await client.delete(f"/plans/{plan_id}", headers=headers)
    assert del_res.status_code == 200


@pytest.mark.asyncio
async def test_get_all_plans(client):
    res = await client.get("/plans/")

    # Debugging: Print the response if the test fails
    if res.status_code != 200:
        print("Test Get All Plans Failed")
        print("Response Status Code:", res.status_code)
        print("Response JSON:", res.json())

    assert res.status_code == 200
    assert res.json()["ok"] is True
    assert isinstance(res.json()["data"], list)


@pytest.mark.asyncio
async def test_get_plan_by_id(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Create a plan first
    plan_data = {
        "name": "Test Plan for Get By ID",
        "price": 99,
        "duration_days": 30,
        "features": ["feature1", "feature2"],
    }
    create_res = await client.post("/plans/", json=plan_data, headers=headers)
    assert create_res.status_code == 200
    plan_id = create_res.json()["data"]["id"]

    # Retrieve the plan by ID
    res = await client.get(f"/plans/{plan_id}")
    if res.status_code != 200:
        print("Test Get Plan By ID Failed")
        print("Response Status Code:", res.status_code)
        print("Response JSON:", res.json())

    assert res.status_code == 200
    assert res.json()["ok"] is True
    assert res.json()["data"]["id"] == plan_id

    # Clean up: Delete the created plan
    del_res = await client.delete(f"/plans/{plan_id}", headers=headers)
    assert del_res.status_code == 200


@pytest.mark.asyncio
async def test_update_plan(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Create a plan first
    plan_data = {
        "name": "Test Plan for Update",
        "price": 99,
        "duration_days": 30,
        "features": ["feature1", "feature2"],
    }
    create_res = await client.post("/plans/", json=plan_data, headers=headers)
    assert create_res.status_code == 200
    plan_id = create_res.json()["data"]["id"]

    # Update the plan
    updated_plan_data = {
        "name": "Updated Plan",
        "price": 199,
        "duration_days": 60,
        "features": ["feature1", "feature3"],
    }
    res = await client.put(f"/plans/{plan_id}", json=updated_plan_data, headers=headers)
    if res.status_code != 200:
        print("Test Update Plan Failed")
        print("Response Status Code:", res.status_code)
        print("Response JSON:", res.json())

    assert res.status_code == 200
    assert res.json()["ok"] is True
    assert res.json()["data"]["name"] == "Updated Plan"
    assert res.json()["data"]["price"] == 199

    # Clean up: Delete the updated plan
    del_res = await client.delete(f"/plans/{plan_id}", headers=headers)
    assert del_res.status_code == 200


@pytest.mark.asyncio
async def test_delete_plan(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Create a plan first
    plan_data = {
        "name": "Test Plan for Delete",
        "price": 99,
        "duration_days": 30,
        "features": ["feature1", "feature2"],
    }
    create_res = await client.post("/plans/", json=plan_data, headers=headers)
    assert create_res.status_code == 200
    plan_id = create_res.json()["data"]["id"]

    # Delete the plan
    res = await client.delete(f"/plans/{plan_id}", headers=headers)
    if res.status_code != 200:
        print("Test Delete Plan Failed")
        print("Response Status Code:", res.status_code)
        print("Response JSON:", res.json())

    assert res.status_code == 200
    assert res.json()["ok"] is True

    # Verify the plan no longer exists
    get_res = await client.get(f"/plans/{plan_id}")
    assert get_res.status_code == 404
