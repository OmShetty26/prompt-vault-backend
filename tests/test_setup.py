from sqlalchemy import text


def test_test_database_is_available(db_session):
    result = db_session.execute(text("SELECT 1"))

    assert result.scalar_one() == 1


def test_openapi_schema_is_available(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "paths" in response.json()