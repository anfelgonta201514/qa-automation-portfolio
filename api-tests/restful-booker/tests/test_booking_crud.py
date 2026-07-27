from utils.schemas import CreateBookingResponse


def test_create_booking_valid_schema(api_client, booking_payload):
    response = api_client.create_booking(booking_payload)

    assert response.status_code == 200
    # Si el JSON no tiene exactamente esta forma (campos faltantes, tipos
    # incorrectos), pydantic lanza ValidationError y el test falla solo.
    CreateBookingResponse(**response.json())

def test_get_booking_returns_created_data(api_client, created_booking):
    booking_id, payload = created_booking
    response = api_client.get_booking(booking_id)
    assert response.status_code == 200
    assert response.json()["firstname"] == payload["firstname"]

def test_get_booking_nonexistent_id_returns_404(api_client):
    response = api_client.get_booking(999999999)
    assert response.status_code == 404

def test_update_booking_with_valid_token(api_client, auth_token, created_booking):
    booking_id, payload = created_booking
    payload["lastname"] = "Editado"
    response = api_client.update_booking(booking_id, payload, auth_token)
    assert response.status_code == 200
    assert response.json()["lastname"] == payload["lastname"]

def test_update_booking_without_token_returns_403(api_client, created_booking):
    booking_id, payload = created_booking
    payload["lastname"] = "Editado"
    response = api_client.update_booking(booking_id, payload)
    assert response.status_code == 403
