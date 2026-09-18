import json

import allure


def attach_response(response, name: str) -> None:
    """Adjunta el body de una respuesta HTTP al reporte de Allure. Mismo
    principio que attach_screenshot() en la suite de UI: úsalo solo en
    puntos de validación (justo antes del assert), no en cada llamada."""
    try:
        body = json.dumps(response.json(), indent=2, ensure_ascii=False)
        attachment_type = allure.attachment_type.JSON
    except ValueError:
        body = response.text
        attachment_type = allure.attachment_type.TEXT
    allure.attach(body, name=name, attachment_type=attachment_type)
