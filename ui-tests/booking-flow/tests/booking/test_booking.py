import uuid

from playwright.sync_api import expect


def test_booking_valid_data_reservation_confirmed(pages):
    home = pages["home"]
    booking = pages["booking"]

    home.goto()
    home.select_dates()
    home.search_availability()
    home.book_room(2)

    unique_id = uuid.uuid4().hex[:8]

    booking.click_reserve_now()
    booking.fill_first_name("Andres")
    booking.fill_last_name("Gonzalez")
    booking.fill_email(f"andres.{unique_id}@example.com")
    booking.fill_phone("32112311223")
    booking.click_reserve_now()

    expect(booking.page.get_by_text("Booking Confirmed")).to_be_visible()
