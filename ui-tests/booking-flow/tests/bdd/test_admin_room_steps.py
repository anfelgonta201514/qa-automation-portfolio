import random

from playwright.sync_api import expect
from pytest_bdd import given, scenarios, then, when

from utils.allure_helpers import attach_screenshot

scenarios("../../features/admin_room.feature")


@given("que inicio sesión como administrador")
def admin_login(pages):
    pages["home"].goto()
    admin = pages["admin"]
    admin.goto_admin_login()
    admin.type_admin_username("admin")
    admin.type_admin_password("password")
    admin.click_admin_login_button()

    # Validación real de que el login funcionó (no solo una acción). Se
    # espera tanto que aparezca lo nuevo (Logout) como que desaparezca lo
    # viejo (el input de usuario): en una SPA con transición client-side,
    # confiar solo en "apareció Logout" puede capturar el screenshot a
    # medio camino, con el formulario de login todavía visible.
    expect(admin.admin_logout_option_button).to_be_visible()
    expect(admin.admin_username_input).to_be_hidden()
    # Además del cambio de formulario, la SPA sigue cargando contenido async
    # tras el login (spinner "Loading..."): esperarlo evita un screenshot a
    # medio cargar.
    expect(admin.page.get_by_text("Loading...").first).to_be_hidden()
    attach_screenshot(admin.page, "Login de administrador exitoso")


@when("que creo una habitación nueva con tipo, precio y servicios", target_fixture="room_number")
def admin_rooms_create(pages):
    room_number = str(random.randint(200, 9999))
    admin = pages["admin"]
    admin.goto_admin_rooms()
    admin.type_admin_rooms_name(room_number)
    admin.select_admin_rooms_type("Single")
    admin.select_admin_rooms_accessible("true")
    admin.type_admin_rooms_price("111")
    admin.check_amenity("WiFi")
    admin.check_amenity("Safe")
    admin.click_admin_rooms_create()
    return room_number

@then("que la habitación aparece en el listado de habitaciones correctamente")
def admin_rooms_list(pages, room_number):
    admin = pages["admin"]
    expect(admin.page.locator(f"#roomName{room_number}")).to_be_visible()
    attach_screenshot(admin.page, f"Habitación {room_number} creada")

