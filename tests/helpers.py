def register_user(client, username="alice_test", password="samplePassword123"):
    response = client.post(
        "/auth/register",
        json={"username": username, "password": password},
    )
    assert response.status_code == 201, response.text
    return response.json()


def login_user(client, username="alice_test", password="samplePassword123"):
    response = client.post(
        "/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()


def register_and_login(client, username="alice_test", password="samplePassword123"):
    user = register_user(client, username, password)
    login_user(client, username, password)
    return user

def create_prompt(client, title="test_prompt", content="Sample Text", category="debug"):
    response = client.post(
        "/api/prompts", 
        json= {"title": title, "content": content, "category": category}
    )
    assert response.status_code == 200
    return response.json()