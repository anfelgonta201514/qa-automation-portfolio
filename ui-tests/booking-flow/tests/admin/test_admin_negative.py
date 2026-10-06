from playwright.sync_api import expect

from utils.allure_helpers import attach_screenshot


def test_admin_login_invalid_credentials_access_denied(pages):
    home = pages["home"]
    admin = pages["admin"]

    home.goto()
    admin.goto_admin_login()
    admin.type_admin_username("admin")
    admin.type_admin_password("wrong-password")
    admin.click_admin_login_button()

    # La app SÍ muestra un mensaje de error: <div class="alert alert-danger"
    # role="alert">Invalid credentials</div> (verificado el 2026-10-06, 3 de 3
    # corridas; una versión anterior de este test asumía que no existía).
    # Es la señal de que la respuesta del login ya llegó, así que se espera
    # primero: sin esto, los asserts negativos de abajo pasarían al instante,
    # incluso antes de que el servidor respondiera.
    # Timeout de 10 s porque el mensaje tardó entre 0.35 s y 4.96 s en aparecer
    # (latencia de la API), muy cerca del límite por defecto de 5 s.
    expect(admin.admin_login_error_alert).to_be_visible(timeout=10_000)

    # Y el estado negativo: se queda en el formulario de login y nunca
    # aparece la navegación de administrador.
    expect(admin.admin_username_input).to_be_visible()
    expect(admin.admin_rooms_option_button).to_be_hidden()
    attach_screenshot(admin.page, "Login de administrador rechazado")
