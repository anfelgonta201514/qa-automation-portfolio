import uuid

from playwright.sync_api import expect
from pytest_bdd import given, scenarios, then, when

from utils.allure_helpers import attach_screenshot

# scenarios() le dice a pytest-bdd qué .feature ejecutar. La ruta es
# relativa a ESTE archivo. Genera automáticamente una función de test por
# cada Scenario del archivo — no hay que escribir `def test_...` a mano.
scenarios("../../features/booking.feature")


# El texto entre comillas debe coincidir EXACTO (palabra por palabra) con
# la línea del .feature. Reutiliza el fixture `pages` que ya existe en
# conftest.py — no se repite lógica de Playwright aquí, solo se orquesta.
@given("que estoy en la página de inicio de Restful Booker Platform")
def go_to_home(pages):
    pages["home"].goto()


@when("busco disponibilidad y selecciono una habitación")
def search_and_select_room(pages):
    pages["home"].select_dates()
    pages["home"].search_availability()
    pages["home"].book_room(2)


# El "And" del .feature hereda el tipo del paso anterior (When), por eso
# este step se decora con @when aunque en el Gherkin diga "And".
@when("completo el formulario de reserva con datos de contacto válidos")
def fill_booking_form(pages):
    booking = pages["booking"]
    unique_id = uuid.uuid4().hex[:8]

    booking.click_reserve_now()
    booking.fill_first_name("Andres")
    booking.fill_last_name("Gonzalez")
    booking.fill_email(f"andres.{unique_id}@example.com")
    booking.fill_phone("32112311223")
    booking.click_reserve_now()


@then("la reserva queda confirmada")
def assert_confirmation(pages):
    booking_page = pages["booking"].page
    expect(booking_page.get_by_text("Booking Confirmed")).to_be_visible()
    attach_screenshot(booking_page, "Reserva confirmada")
