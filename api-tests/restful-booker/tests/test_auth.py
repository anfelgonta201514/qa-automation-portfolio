from utils.allure_helpers import attach_response


def test_auth_valid_credentials_returns_token(api_client):
    response = api_client.create_token("admin", "password123")
    attach_response(response, "Respuesta de POST /auth con credenciales válidas")
    assert response.status_code == 200
    assert "token" in response.json()

def test_auth_invalid_credentials_returns_no_token(api_client):
    response = api_client.create_token("admin", "wrong-password")
    attach_response(response, "Respuesta de POST /auth con credenciales inválidas")
    assert response.status_code == 200
    assert "token" not in response.json()
    assert response.json().get("reason") == "Bad credentials"