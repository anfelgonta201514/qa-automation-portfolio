# ui-tests/booking-flow

Suite Playwright + pytest contra [Restful Booker Platform](https://automationintesting.online), app open source de Mark Winteringham / Richard Bradshaw pensada para practicar automatización UI + API.

## Qué prueba

Flujo de reserva de habitación de hotel: home (listado de habitaciones) → detalle de habitación → reserva (fechas + datos de contacto) → confirmación. Además, formulario de contacto y panel de administración (login + gestión de habitaciones/reservas).

## Decisión de diseño: reset de datos

La app resetea sus datos cada ~10 minutos al estado inicial. Por eso cada test crea sus propios datos de principio a fin (no asume habitaciones o reservas preexistentes), evitando dependencias de estado entre ejecuciones.

## Arquitectura

- `config/init.json` — configuración (BASE_URL, modo headless, etc.)
- `utils/config.py` — carga la config como clase estática
- `pages/` — Page Object Model: `base_page.py` + un page object por pantalla
- `conftest.py` — fixtures de Playwright (browser/context/page) + captura de traza y screenshot en fallos
- `tests/booking/` — casos de prueba

## Estado

🔄 En construcción — ver [plan de estudio](../../README.md).
