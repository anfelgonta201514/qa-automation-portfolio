import pytest

from utils.booking_client import BookingClient
from utils.config import ADMIN_PASSWORD, ADMIN_USERNAME, BASE_URL


@pytest.fixture(scope="session")
def api_client():
    return BookingClient(BASE_URL)


@pytest.fixture(scope="session")
def auth_token(api_client):
    response = api_client.create_token(ADMIN_USERNAME, ADMIN_PASSWORD)
    return response.json()["token"]


@pytest.fixture
def booking_payload():
    return {
        "firstname": "Andres",
        "lastname": "Gonzalez",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-08-01", "checkout": "2026-08-05"},
        "additionalneeds": "Breakfast",
    }


@pytest.fixture
def created_booking(api_client, auth_token, booking_payload):
    """Crea una reserva propia del test y la borra al terminar, sin
    depender de datos preexistentes en la API (mismo principio que en la
    suite de UI: cada test es dueño de sus propios datos)."""
    response = api_client.create_booking(booking_payload)
    booking_id = response.json()["bookingid"]
    yield booking_id, booking_payload
    api_client.delete_booking(booking_id, auth_token)
