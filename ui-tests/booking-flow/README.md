# ui-tests/booking-flow

Suite Playwright + pytest contra [Restful Booker Platform](https://automationintesting.online), app open source de Mark Winteringham / Richard Bradshaw pensada para practicar automatización UI + API.

## Qué prueba

- **Booking flow** (`tests/booking/test_booking.py`): home (listado de habitaciones) → seleccionar fechas → elegir habitación → reserva (datos de contacto) → confirmación.
- **Admin** (`tests/admin/test_admin_options.py`): login de administrador, navegación entre secciones (Rooms/Report), y creación de una habitación nueva.

## Decisiones de diseño

**Reset de datos.** La app resetea sus datos cada ~10 minutos al estado inicial. Por eso cada test crea sus propios datos de principio a fin (email de contacto y número de habitación generados dinámicamente), evitando dependencias de estado entre ejecuciones y falsos positivos si un test corre dos veces dentro de la misma ventana de reset.

**Fechas dinámicas en el datepicker.** El calendario de reserva genera celdas con `aria-label` tipo `"Choose Friday, 10 July"`, ligado a la fecha real del día. Hardcodear ese texto rompería el test al día siguiente, así que `HomePage._gridcell_label()` lo calcula a partir de `date.today() + timedelta(...)`.

**La tabla de habitaciones de Admin no es HTML semántico.** Visualmente `/admin/rooms` se ve como una tabla, pero el aria snapshot reveló que está construida con `<p>` en un grid CSS, sin `<table>` ni `role="row"`. Por eso la verificación de que una habitación se creó usa `get_by_text(room_number, exact=True)` en vez de `get_by_role("row", ...)`. Lección general: no asumir semántica HTML por apariencia visual — verificar siempre con el aria snapshot antes de elegir el locator.

**Validación de teléfono.** El campo `Phone` del formulario de contacto rechaza números de 10 dígitos y acepta 11 — candidato a caso de prueba negativo explícito más adelante (semana 5, validaciones de formulario/API).

## Arquitectura

- `config/init.json` — configuración (BASE_URL, modo headless, etc.)
- `utils/config.py` — carga la config como clase estática
- `pages/` — Page Object Model: `base_page.py`, `home_page.py`, `booking_page.py`, `admin_page.py`
- `conftest.py` — fixtures de Playwright (browser/context/page/pages) + captura de traza y screenshot en fallos
- `tests/booking/` y `tests/admin/` — casos de prueba

## Cómo correr

```bash
cd ui-tests/booking-flow
../../.venv/Scripts/pytest -v
```

## Estado

🔄 En construcción — booking flow y admin básico funcionando (`PASSED`). Pendiente: patrón de datos parametrizados (TR/battery) y casos negativos explícitos. Ver [plan de estudio](../../README.md).
