# ui-tests/booking-flow

Suite Playwright + pytest contra [Restful Booker Platform](https://automationintesting.online), app open source de Mark Winteringham / Richard Bradshaw pensada para practicar automatización UI + API.

## Qué prueba

- **Booking flow** (`tests/booking/test_booking.py`): home (listado de habitaciones) → seleccionar fechas → elegir habitación → reserva (datos de contacto) → confirmación.
- **Admin** (`tests/admin/test_admin_options.py`): login de administrador, navegación entre secciones (Rooms/Report), y creación de una habitación nueva.
- **Batería de datos** (`tests/battery/`): mismo flujo de creación de habitaciones y de reserva, parametrizado desde Excel (`data/room_battery.xlsx`, `data/booking_battery.xlsx`) para cubrir múltiples combinaciones sin duplicar código de test.

## Decisiones de diseño

**Reset de datos.** La app resetea sus datos cada ~10 minutos al estado inicial. Por eso cada test crea sus propios datos de principio a fin (email de contacto y número de habitación generados dinámicamente), evitando dependencias de estado entre ejecuciones y falsos positivos si un test corre dos veces dentro de la misma ventana de reset.

**Fechas dinámicas en el datepicker.** El calendario de reserva genera celdas con `aria-label` tipo `"Choose Friday, 10 July"`, ligado a la fecha real del día. Hardcodear ese texto rompería el test al día siguiente, así que `HomePage._gridcell_label()` lo calcula a partir de `date.today() + timedelta(...)`.

**La tabla de habitaciones de Admin no es HTML semántico.** Visualmente `/admin/rooms` se ve como una tabla, pero el aria snapshot reveló que está construida con `<p>` en un grid CSS, sin `<table>` ni `role="row"`. La verificación de que una habitación se creó usa el id estable de cada celda (`#roomName{numero}`), no `get_by_text`, porque el texto del número de habitación puede coincidir por casualidad con el del precio (ambos son `<p>` sueltos) y produce un *strict mode violation* de Playwright. Lección general: no asumir semántica HTML por apariencia visual — verificar siempre con el aria snapshot antes de elegir el locator, y preferir un id estable sobre texto cuando exista.

**Validación de teléfono.** El campo `Phone` del formulario de contacto rechaza números de 10 dígitos y acepta 11 — candidato a caso de prueba negativo explícito más adelante (semana 5, validaciones de formulario/API).

**Números de habitación fijos en la batería, con sufijo aleatorio.** `room_battery.xlsx` usa números de habitación fijos (200-204) a propósito, como en el patrón de TR con datos hardcodeados de Selenium. Eso es seguro dentro de una sola corrida, pero si dos ejecuciones caen dentro de la misma ventana de reset de ~10 min de la app (pasa fácil disparando varios runs de CI seguidos durante desarrollo activo), un número fijo choca con uno ya creado por la corrida anterior y produce un `id` duplicado en el DOM (la app no valida unicidad de IDs), rompiendo el `expect()` con un *strict mode violation*. Se resuelve enviando `{número_base}{sufijo aleatorio de 2 dígitos}`: el número base sigue viniendo del Excel (legible, trazable al escenario en el reporte), pero el valor real enviado es único por ejecución — mismo principio que ya se aplicó al email del booking.

**Batería de datos y tipos de pandas.** Al leer Excel con pandas, columnas que solo contienen dígitos o `true`/`false` se auto-infieren como `int`/`bool`, no como texto — y Playwright exige `str` en `.fill()`/`.select_option()`. Se resuelve en dos niveles: `battery_loader.load_battery()` acepta un `dtype` explícito por columna (usado para `phone`), y `AdminPage.select_admin_rooms_accessible()` normaliza el valor con `str(option).lower()` para aceptar tanto bool como string sin importar la fuente del dato.

**Paralelismo (`pytest-xdist`) contra un servidor de demo compartido.** Correr la batería con `-n` abre varios navegadores simultáneos contra `automationintesting.online`, un servicio gratuito no pensado para alta concurrencia. Ocasionalmente un worker puede recibir un error de red genuino (página de error nativa del navegador, no un fallo de aserción) si el servidor no responde a tiempo. Es flakiness de infraestructura compartida, no del código — si se vuelve frecuente, bajar el número de workers (`-n 3`/`-n 4`) reduce la probabilidad.

**El flujo de booking falla de forma consistente desde GitHub Actions (no localmente).** El mismo test que pasa siempre en local (headed o headless) falla el 100% de las veces al correr desde el runner de GitHub, justo después de confirmar la reserva, con el error nativo `"This page couldn't load"` — indicando un fallo real de red al navegar, no un problema de aserción. Confirmado que no es un tema de headless (pasa igual en headless local con `CI=true`). La hipótesis más probable es que el sitio bloquea o limita tráfico desde rangos de IP de datacenter/nube (protección anti-bot común), algo fuera de nuestro control. Por eso en CI (`.github/workflows/tests.yml`) el step de booking corre con `continue-on-error: true`: se ejecuta, se reporta, sube sus artifacts, pero no bloquea el build — a diferencia de Admin/Rooms, que sí son bloqueantes porque nunca han fallado. Es una decisión explícita para no ensuciar el badge con la limitación de un tercero, sin ocultar el problema.

**Config local vs pipeline.** `config/init.json` es para ejecución local (headless configurable, valores cómodos para debug); `config/remote_config.json` es lo que usa CI (headless siempre `true`, no hay pantalla en el runner) — mismo patrón que en el proyecto de Selenium. `Config` elige el archivo según la variable de entorno `CI` (que GitHub Actions define automáticamente), sin mezclar lógica de entorno con los datos de configuración. El navegador (`BROWSER`) sí se sobreescribe puntualmente por variable de entorno porque la matrix de CI necesita 3 navegadores distintos en la misma corrida, algo que un solo archivo estático no puede representar.

## Arquitectura

- `config/init.json` / `config/remote_config.json` — configuración local vs pipeline (BASE_URL, modo headless, etc.)
- `utils/config.py` — carga la config como clase estática, según el entorno
- `utils/battery_loader.py` — lee un `.xlsx` de `data/` y devuelve `list[dict]` para parametrizar tests
- `pages/` — Page Object Model: `base_page.py`, `home_page.py`, `booking_page.py`, `admin_page.py`
- `conftest.py` — fixtures de Playwright (browser/context/page/pages) + captura de traza y screenshot en fallos
- `data/` — Excel con los escenarios de la batería
- `tests/booking/`, `tests/admin/`, `tests/battery/` — casos de prueba

## Cómo correr

```bash
cd ui-tests/booking-flow

# Toda la suite
pytest -v

# Solo una batería, en paralelo, con reporte Allure
pytest tests/battery -v -n 4 -m room_battery --alluredir=allure-results
pytest tests/battery -v -n 4 -m booking_battery --alluredir=allure-results
```

## Estado

✅ Booking flow, Admin y batería de datos parametrizada funcionando. Pendiente: casos negativos explícitos (teléfono inválido, credenciales de admin incorrectas). Ver [plan de estudio](../../README.md).
