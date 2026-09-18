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

    # La app no muestra ningún mensaje de error en el DOM ante credenciales
    # inválidas (verificado: la respuesta de /api/auth/login trae el error,
    # pero no se renderiza) — la señal real de que el login falló es que
    # se queda en el formulario de login y nunca aparece la navegación de
    # administrador.
    expect(admin.admin_username_input).to_be_visible()
    expect(admin.admin_rooms_option_button).to_be_hidden()
    attach_screenshot(admin.page, "Login de administrador rechazado")
