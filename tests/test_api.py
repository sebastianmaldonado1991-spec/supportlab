import pytest

from app import app
from init_db import initialize_database


@pytest.fixture(autouse=True)
def reset_database():
    """
    Reinicia la base antes de cada prueba para que todas comiencen
    con los mismos tres usuarios.
    """

    initialize_database()


@pytest.fixture
def client():
    """Crea un cliente de pruebas para enviar solicitudes a Flask."""

    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_health_returns_200(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["service"] == "SupportLab"
    assert data["status"] == "ok"
    assert data["database"] == "available"


def test_get_existing_user(client):
    response = client.get("/users/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["name"] == "Ana Torres"
    assert data["status"] == "active"


def test_get_missing_user_returns_404(client):
    response = client.get("/users/99")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "user_not_found"
    assert data["user_id"] == 99


def test_list_active_users(client):
    response = client.get("/users?status=active")

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 2

    for user in data["users"]:
        assert user["status"] == "active"


def test_invalid_status_filter_returns_400(client):
    response = client.get("/users?status=pending")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "invalid_status"


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Martín López",
            "email": "martin@example.com",
            "status": "active"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Martín López"
    assert data["email"] == "martin@example.com"
    assert data["status"] == "active"


def test_duplicate_email_returns_409(client):
    new_user = {
        "name": "Martín López",
        "email": "martin@example.com",
        "status": "active"
    }

    first_response = client.post("/users", json=new_user)
    second_response = client.post("/users", json=new_user)

    assert first_response.status_code == 201
    assert second_response.status_code == 409

    error_data = second_response.get_json()

    assert error_data["error"] == "email_already_exists"
    assert error_data["email"] == "martin@example.com"

    users_response = client.get("/users")
    users_data = users_response.get_json()

    matching_users = [
        user
        for user in users_data["users"]
        if user["email"] == "martin@example.com"
    ]

    assert len(matching_users) == 1


def test_update_user_status(client):
    response = client.patch(
        "/users/2/status",
        json={
            "status": "active"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 2
    assert data["status"] == "active"