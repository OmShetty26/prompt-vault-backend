from tests.helpers import create_prompt, login_user, register_and_login

def test_create_prompt_success(client, authenticated_user):
    prompt_payload = {
        "title": "test_prompt_1",
        "content": "This is a sample prompt...",
        "category": "debug"
    }

    prompt_response = client.post("/api/prompts", json=prompt_payload)

    assert prompt_response.status_code == 200

    prompt_data = prompt_response.json()
    assert prompt_data["id"] is not None
    assert prompt_data["title"] == prompt_payload['title']
    assert prompt_data["content"] == prompt_payload['content']
    assert prompt_data["category"] == prompt_payload['category']


def test_list_prompts_returns_current_users_prompts(client):
    register_and_login(client, username="user_1")
    prompt_1 = create_prompt(client, title="prompt 1")
    client.post("/auth/logout")

    register_and_login(client, username="user_2")
    prompt_2 = create_prompt(client, title="prompt 2")
    client.post("/auth/logout")

    login_user(client, username="user_1")
    prompts_response = client.get("/api/prompts")
    assert prompts_response.status_code == 200

    prompts_list = prompts_response.json()

    prompt_ids = {prompt["id"] for prompt in prompts_list}

    assert prompt_1["id"] in prompt_ids
    assert prompt_2["id"] not in prompt_ids


def test_get_own_prompt_success(client, authenticated_user):
    user_prompt = create_prompt(client, title="test_prompt", content="Sample text")
    db_response = client.get(f"/prompt/{user_prompt['id']}")
    assert db_response.status_code == 200

    db_prompt = db_response.json()
    assert user_prompt == db_prompt


def test_update_own_prompt_success(client, authenticated_user):
    upd_payload = {
        "title" : "Updated Test Prompt",
        "content" : "New Sample",
        "category" : "debug"
    }

    og_prompt = create_prompt(client)
    update_response = client.put(f"/prompt/{og_prompt['id']}", json=upd_payload)
    assert update_response.status_code == 200

    updated_prompt = update_response.json()
    assert updated_prompt['id'] == og_prompt['id']
    assert updated_prompt['title'] == upd_payload['title']
    assert updated_prompt['content'] == upd_payload['content']
    assert updated_prompt['category'] == upd_payload['category']


def test_delete_own_prompt_success(client, authenticated_user):
    user_prompt = create_prompt(client)
    delete_response = client.delete(f"/prompt/{user_prompt['id']}")
    assert delete_response.status_code == 200

    new_response = client.get(f"/prompt/{user_prompt['id']}")
    assert new_response.status_code == 404


def test_create_prompt_rejects_invalid_payload(client, authenticated_user):
    payload = {
        "title": "Invalid sample",
        "content": "",
        "category": "debug"
    }
    invalid_response = client.post("/api/prompts", json=payload)
    assert invalid_response.status_code == 400


def test_get_missing_prompt_returns_404(client, authenticated_user):
    missing_response = client.get("/prompt/99999")
    assert missing_response.status_code == 404


def test_user_cannot_get_another_users_prompt(client):
    register_and_login(client, username="user_1")
    prompt_1 = create_prompt(client, title="prompt 1")
    client.post("/auth/logout")

    register_and_login(client, username="user_2")
    unauth_response = client.get(f"/prompt/{prompt_1['id']}")
    assert unauth_response.status_code == 404


def test_user_cannot_update_another_users_prompt(client):
    update_payload = {
        "title": "Attempted unauthorized update",
        "content": "Updated sample content",
        "category": "debug",
    }

    register_and_login(client, username="user_1")
    prompt_1 = create_prompt(client, title="prompt 1")
    client.post("/auth/logout")

    register_and_login(client, username="user_2")

    response = client.put(
        f"/prompt/{prompt_1['id']}",
        json=update_payload,
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_prompt(client):
    register_and_login(client, username="user_1")
    prompt_1 = create_prompt(client, title="prompt 1")
    client.post("/auth/logout")

    register_and_login(client, username="user_2")
    unauth_response = client.delete(f"/prompt/{prompt_1['id']}")
    assert unauth_response.status_code == 404




