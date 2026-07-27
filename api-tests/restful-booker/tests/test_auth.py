
def test_auth_valid_credentials_returns_token(api_client):
    response = api_client.create_token("admin", "password123")
    assert response.status_code == 200
    assert "token" in response.json()

def test_auth_invalid_credentials_returns_no_token(api_client):
    response = api_client.create_token("admin", "wrong-password")
    assert response.status_code == 200
    assert "token" not in response.json()
    assert response.json().get("reason") == "Bad credentials"