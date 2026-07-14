import requests


class BookingClient:
    """Encapsula las llamadas HTTP a restful-booker. Mismo rol que un Page
    Object en la suite de UI: el test no arma URLs ni headers a mano."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def ping(self):
        return self.session.get(f"{self.base_url}/ping")

    def create_token(self, username: str, password: str):
        return self.session.post(
            f"{self.base_url}/auth",
            json={"username": username, "password": password},
        )

    def create_booking(self, payload: dict):
        return self.session.post(f"{self.base_url}/booking", json=payload)

    def get_booking(self, booking_id: int):
        return self.session.get(f"{self.base_url}/booking/{booking_id}")

    def get_booking_ids(self, **filters):
        return self.session.get(f"{self.base_url}/booking", params=filters)

    def update_booking(self, booking_id: int, payload: dict, token: str):
        return self.session.put(
            f"{self.base_url}/booking/{booking_id}",
            json=payload,
            cookies={"token": token},
        )

    def delete_booking(self, booking_id: int, token: str):
        return self.session.delete(
            f"{self.base_url}/booking/{booking_id}",
            cookies={"token": token},
        )
