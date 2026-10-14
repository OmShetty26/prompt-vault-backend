### Registration Tests
def test_register_user_success(client):
    # Arrange: prepare valid registration data
    payload = {
        "username": "alice_test",
        "password": "samplePassword123"
    }

    # Act: send the registration request
    response = client.post("/auth/register", json=payload)

    # Assert: check the validity of the payload
    assert response.status_code == 201

    response_data = response.json()

    assert response_data["username"] == payload["username"]
    assert "password" not in response_data
    assert "password_hash" not in response_data
    assert response_data["id"] is not None


def test_register_rejects_short_username(client):
    payload = {
        "username": "ab",
        "password": "samplepassword123"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_register_rejects_invalid_username_characters(client):
    payload = {
        "username": "alice-test",
        "password": "samplepassword123"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_register_rejects_short_password(client):
    payload = {
        "username": "alice_test",
        "password": "pwd123"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_register_rejects_duplicate_username(client):
    payload = {
        "username": "dup1_user",
        "password": "samplepassword123"
    }

    response = client.post("/auth/register", json=payload)
    response_2 = client.post("/auth/register", json=payload)

    assert response_2.status_code == 409

### Login Tests
def test_login_success(client):
    # Arrange: prepare valid registration data
    payload = {
        "username": "alice_test",
        "password": "samplePassword123"
    }

    # Act: send the registration request
    reg_response = client.post("/auth/register", json=payload)
    user_response = client.post("/auth/login", json=payload)

    # Assert: check the validity of the payload
    assert user_response.status_code == 200

    user_response_data = user_response.json()

    assert user_response_data["username"] == payload["username"]
    assert "password" not in user_response_data
    assert "password_hash" not in user_response_data
    assert user_response_data["id"] is not None

    set_cookie_header = user_response.headers.get("set-cookie", "")
    
    # Check if the token name and HttpOnly attribute are explicitly in the header string
    assert "access_token" in set_cookie_header
    assert "HttpOnly" in set_cookie_header

def test_login_rejects_wrong_password(client):
    # Arrange: prepare valid registration data
    payload = {
        "username": "alice_test",
        "password": "samplePassword123"
    }

    payload_incorrect = {
        "username": "alice_test",
        "password": "wrongPassword123"
    }

    # Act: send the registration request
    reg_response = client.post("/auth/register", json=payload)
    user_response = client.post("/auth/login", json=payload_incorrect)

    # Assert: check the validity of the payload
    assert user_response.status_code == 401


def test_login_rejects_unknown_username(client):
    # Arrange: prepare valid registration data
    payload = {
        "username": "unknownUsername",
        "password": "samplePassword123"
    }

    # Act: send the registration request
    user_response = client.post("/auth/login", json=payload)

    # Assert: check the validity of the payload
    assert user_response.status_code == 401


### Session Behavior Tests
def test_auth_me_returns_logged_in_user(client):
    # Arrange: prepare valid registration data
    payload = {
        "username": "alice_test",
        "password": "samplePassword123"
    }

    # Act: send the registration request
    reg_response = client.post("/auth/register", json=payload)
    login_response = client.post("/auth/login", json=payload)
    user_response = client.get("/auth/me")

    assert user_response.status_code == 200

    login_data = login_response.json()
    user_data = user_response.json()
    
    assert user_data['id'] == login_data['id']
    assert user_data['username'] == login_data['username']


def test_auth_me_returns_unauthenticated_user(client):
    user_response = client.get("/auth/me")

    assert user_response.status_code == 401


def test_logout_clears_session(client):
    # Arrange: prepare valid registration data
    payload = {
        "username": "alice_test",
        "password": "samplePassword123"
    }

    # Act: send the registration request
    reg_response = client.post("/auth/register", json=payload)
    login_response = client.post("/auth/login", json=payload)
    logout_response = client.post("/auth/logout")

    assert logout_response.status_code == 200

    user_response = client.get("/auth/me")

    assert user_response.status_code == 401
