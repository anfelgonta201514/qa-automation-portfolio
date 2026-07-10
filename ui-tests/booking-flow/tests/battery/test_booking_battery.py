import uuid

import pytest
from playwright.sync_api import expect

from utils.battery_loader import load_battery

# Se carga una sola vez, cuando pytest importa el archivo (no en cada test).
BOOKING_SCENARIOS = load_battery("booking_battery.xlsx", dtype={"phone": str})


@pytest.mark.parametrize(
    "scenario",
    BOOKING_SCENARIOS,
    ids=[s["scenario_id"] for s in BOOKING_SCENARIOS],
)
@pytest.mark.booking_battery
def test_booking_battery(pages, scenario):
    home = pages["home"]
    booking = pages["booking"]

    home.goto()
    home.select_dates(scenario['nights_from_today'], scenario['stay_length'])
    home.search_availability()
    home.book_room(2)

    unique_id = uuid.uuid4().hex[:8]

    booking.click_reserve_now()
    booking.fill_first_name(scenario['firstname'])
    booking.fill_last_name(scenario['lastname'])
    booking.fill_email(f"{scenario['scenario_id']}.{unique_id}@example.com")
    booking.fill_phone(scenario['phone'])
    booking.click_reserve_now()

    expect(booking.page.get_by_text("Booking Confirmed")).to_be_visible()
