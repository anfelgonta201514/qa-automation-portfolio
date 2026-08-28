import allure


def attach_screenshot(page, name: str) -> None:
    """Adjunta un screenshot al reporte de Allure. Úsalo solo en puntos de
    validación (Then / asserts), no en cada acción intermedia — el reporte
    debe mostrar evidencia de lo que se confirmó, no un flipbook completo."""
    allure.attach(page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)
