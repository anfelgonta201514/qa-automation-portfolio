def test_create_booking_missing_required_field_returns_500(api_client):
    incomplete_payload = {
        "lastname": "Gonzalez",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-08-01", "checkout": "2026-08-05"},
    }
    response = api_client.create_booking(incomplete_payload)
    assert response.status_code == 500  # comportamiento real, aunque incorrecto

def test_ping_returns_201(api_client):
    response = api_client.ping()
    assert response.status_code == 201  # quirk conocido, no 200

def test_delete_booking_removes_it(api_client, auth_token, booking_payload):
    create_response = api_client.create_booking(booking_payload)
    booking_id = create_response.json()["bookingid"]

    delete_response = api_client.delete_booking(booking_id, auth_token)
    assert delete_response.status_code == 201  # quirk: no 200/204

    get_response = api_client.get_booking(booking_id)
    assert get_response.status_code == 404