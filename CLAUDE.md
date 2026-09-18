# CLAUDE.md — qa-automation-portfolio

Instrucciones permanentes para trabajar en este repo. Esto es lo que **no cambia** de sesión a sesión — arquitectura estable, convenciones y reglas duras.

> **Para estado actual, pendientes, y "qué estábamos haciendo antes de esto"** → ver [`CONTEXT.md`](CONTEXT.md). Ese archivo sí cambia seguido y se actualiza cada vez que avanza el trabajo; este no.

---

## Descripción del proyecto

Portafolio público de QA Automation de Andres Gonzalez (QE en FLYR), pensado para CV/LinkedIn y entrevistas técnicas. Demuestra, con código real y funcionando, el stack que pide el mercado 2026: UI testing, API testing, CI/CD, contenedores y BDD — todo contra **aplicaciones públicas de práctica**, nunca contra el entorno de trabajo real del empleador.

URL: https://github.com/anfelgonta201514/qa-automation-portfolio

---

## Arquitectura general

Dos suites de test independientes, cada una con su propio `pytest.ini`, comparten un `requirements.txt` en la raíz:

```
qa-automation-portfolio/
├── Dockerfile                 # una sola imagen, usada en local y en CI
├── requirements.txt           # dependencias de AMBAS suites (un solo archivo)
├── .github/workflows/tests.yml
├── api-tests/restful-booker/  # pytest + requests contra restful-booker.herokuapp.com
│   ├── conftest.py            # fixtures: api_client, auth_token, created_booking
│   ├── utils/                 # BookingClient (wrapper HTTP, rol de Page Object), schemas pydantic
│   └── tests/
└── ui-tests/booking-flow/     # Playwright + pytest contra automationintesting.online
    ├── conftest.py            # fixtures Playwright: browser/context/page/pages
    ├── config/                # init.json (local) / remote_config.json (CI)
    ├── pages/                 # Page Object Model: BasePage → Home/Booking/AdminPage
    ├── features/ + tests/bdd/ # BDD (Gherkin) — vive AQUÍ, no en la raíz del repo
    ├── data/                  # Excel para el patrón TR/battery
    └── tests/                 # admin/, battery/, bdd/, booking/
```

- **API testing** es independiente de Playwright — no necesita navegador, corre en segundos, va en su propio job de CI.
- **UI testing** sigue Page Object Model estricto: cada pantalla es una clase, el fixture `pages` en `conftest.py` las instancia todas juntas.
- **BDD** no es un framework paralelo — los step definitions en `tests/bdd/` llaman a los mismos Page Objects que usan los tests "planos". Los `.feature` viven dentro de `ui-tests/booking-flow/`, no en una carpeta `features/` en la raíz, para poder importar los Page Objects sin trucos de `sys.path`.
- **Docker** es la misma imagen para todo: se construye una vez y se corre tanto en tu máquina como dentro del workflow de CI (`docker/build-push-action` + `docker run`), nunca se instala Python/Playwright nativo en el runner.

---

## Tecnologías utilizadas

- Python 3.13
- Playwright (sync API) + pytest — UI testing
- requests + pydantic — API testing
- pytest-bdd — BDD/Gherkin
- pandas + openpyxl — carga de datos de batería desde Excel
- pytest-xdist — paralelismo
- pytest-rerunfailures — reintentos ante flakiness de infraestructura externa
- Allure (`allure-pytest` / `allure-pytest-bdd`, mutuamente excluyentes — ver más abajo) — reportes
- Docker (imagen base `mcr.microsoft.com/playwright/python`) — entorno reproducible
- GitHub Actions — CI/CD

---

## Cómo ejecutar el proyecto

**Con Docker (recomendado, no instala nada más que Docker):**
```bash
docker build -t qa-automation-portfolio .
docker run --rm qa-automation-portfolio pytest api-tests/restful-booker -v
docker run --rm -e CI=true qa-automation-portfolio pytest ui-tests/booking-flow -v
```

**Local (Python + venv):**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium firefox webkit
```

---

## Cómo ejecutar los tests

Cada suite se corre desde su propia carpeta (cada una tiene su `pytest.ini`; correrlas desde la raíz del repo con una ruta que no exista ahí hace que pytest **ignore silenciosamente** ese `pytest.ini`):

```bash
# API
cd api-tests/restful-booker
pytest -v

# UI — todo, sin reporte (rápido, para desarrollo)
cd ui-tests/booking-flow
pytest -v

# UI — con reporte Allure, tests normales (admin/booking/batería)
pytest tests/admin tests/battery tests/booking -p allure_pytest --alluredir=allure-results --clean-alluredir

# UI — con reporte Allure BDD (agrega el desglose Given/When/Then)
pytest tests/bdd -p allure_pytest_bdd --alluredir=allure-results-bdd --clean-alluredir

allure serve allure-results
```

`allure-pytest` y `allure-pytest-bdd` están desactivados por defecto en `pytest.ini` (`-p no:...`) porque no pueden estar activos a la vez (ver "Restricciones técnicas"). Para no escribir el comando completo cada vez, `pytest.ini` tiene dos bloques comentados — descomentar **uno solo** y volver a comentarlo después.

En CI no hay que correr nada manual — se dispara con `push`/`pull_request` a `master`, o a mano desde GitHub (Actions → Tests → Run workflow, gracias a `workflow_dispatch`).

---

## Convenciones de código

- **Page Object Model estricto** en UI: un locator/acción vive en la clase de su pantalla, nunca inline en el test. Nombrado tipo `goto_admin_login`, `type_admin_username`, `click_admin_rooms_create` (verbo + qué).
- **Jerarquía de locators**, de mejor a peor: `get_by_role` → `get_by_label` → `get_by_placeholder` → `get_by_text` → `get_by_test_id` → `locator("#id")` → `locator(".clase")` → `locator("[attr]")` → XPath (último recurso). Verificar siempre con el aria snapshot antes de asumir semántica HTML por apariencia visual (esta app tiene "tablas" que en realidad son `<p>` sueltos en un grid CSS).
- **Nunca `time.sleep()` ni waits implícitos** — usar el auto-wait de Playwright y `expect()`.
- **Naming de tests:** `test_[feature]_[scenario]_[expected_result]`.
- **Cada test crea sus propios datos**, con algún componente único (`uuid`, `random`) — la app de UI resetea sus datos cada ~10 min, y un valor fijo puede colisionar con el de una corrida anterior si dos ejecuciones caen dentro de la misma ventana.
- **Config como datos puros**, nunca lógica de entorno mezclada en la clase `Config`: `init.json` para local, `remote_config.json` para pipeline, la clase solo decide qué archivo cargar según `os.environ.get("CI")`.
- **`BookingClient` (API) sigue el mismo principio que un Page Object**: un método por endpoint, el test nunca arma URLs/headers a mano.
- **Capturas de pantalla en Allure (`attach_screenshot()`) solo en puntos de validación** (`Then` / asserts), nunca en cada acción intermedia — el reporte debe mostrar evidencia de lo confirmado, no un flipbook completo.
- **Nunca asumir el comportamiento "correcto" según REST/HTML/convención** sin verificarlo primero contra la app/API real (con `curl`, Postman, o el aria snapshot del error). Varias reglas de este repo existen precisamente porque la app real no se comporta como "debería" (ver Restful-booker: status codes que no siguen REST; SPA con `id`s duplicados en el DOM).

---

## Reglas importantes que debemos respetar

1. **Nunca mezclar nada del entorno de trabajo privado de Andres (SunExpress UAT / FLYR) en este repo.** Ni URLs, ni selectores, ni código, ni capturas. Ese entorno vive en un repo completamente aparte (`playwright-XQ`, privado, TypeScript). Este repo es 100% contra apps públicas de práctica.
2. **Los commits de este repo NO llevan trailer `Co-Authored-By: Claude`.** Es una regla explícita y dura de este repo específico (a diferencia del comportamiento por defecto en otros contextos) — el autor real ya es Andres en todos los commits, la línea solo generaba confusión en el listado de Contributors de GitHub.
3. **Claude no hace `git commit` ni `git push` en este repo salvo que Andres lo pida explícitamente para ese caso puntual.** El flujo normal es: Claude deja los cambios listos en el working directory y avisa; Andres revisa y comitea/pushea él mismo.
4. **`playwright` en `requirements.txt` y el tag de la imagen base del `Dockerfile` deben cambiar SIEMPRE juntos**, a la misma versión exacta (`playwright==X.Y.Z` ↔ `mcr.microsoft.com/playwright/python:vX.Y.Z-noble`). Si se actualiza uno sin el otro, los navegadores de la imagen dejan de ser compatibles con la librería y Playwright rechaza lanzar el browser (el propio error de Playwright dice qué tag necesitas).
5. **Un fallo del "booking flow" en el pipeline de CI es esperado, no es automáticamente una regresión.** Ese flujo (`tests/booking/`, `tests/battery/test_booking_battery.py`) falla consistentemente solo desde runners de GitHub (confirmado que no es headless ni bug de código — el mismo test pasa siempre en local). Está marcado `continue-on-error: true` a propósito. Señal real de bug: que además falle en LOCAL.

---

## Restricciones técnicas

- **`allure-pytest` y `allure-pytest-bdd` NUNCA pueden estar activos al mismo tiempo.** Ambos registran la opción `--alluredir` al cargar el plugin (no solo al usarla) — tenerlos juntos revienta pytest apenas arranca (`ValueError: option names {'--alluredir'} already added`). Es una incompatibilidad documentada del ecosistema Allure (ver `allure-framework/allure-python` issue #486), no un error de configuración propio. Por eso ambos están desactivados por defecto en `ui-tests/booking-flow/pytest.ini` y se reactivan puntualmente, uno a la vez.
- **`allure-pytest-bdd` solo, sin `allure-pytest`, NO sirve para tests planos (no-BDD).** Su listener solo engancha eventos de `pytest-bdd`; un `allure.attach()` dentro de un test normal truena con `KeyError` porque nunca se registró un "item" de Allure para ese test.
- **`--clean-alluredir` no puede vivir en `addopts` por defecto** — es una opción definida por los plugins de Allure, y como ambos están desactivados por defecto, pytest la rechazaría como argumento desconocido en cualquier run normal. Solo va en los comandos/bloques explícitos que también reactivan un plugin de Allure.
- **`pytest.ini` solo se detecta si el comando se corre desde esa carpeta (o una ruta que la tenga como ancestro).** Correr desde la raíz del repo con una ruta que no existe ahí hace que pytest ignore ese `pytest.ini` sin avisar, y los plugins de Allure vuelven a chocar.
- **Windows/Git Bash "traga" rutas estilo Unix** (`/app/...`) al pasarlas a Docker — si algo con volúmenes de Docker da resultados que no cuadran al verificar desde Git Bash, probar desde PowerShell antes de asumir que el problema es real.

---

## Cosas que NO debemos cambiar sin consultarlo

- **La ubicación de `features/` y `tests/bdd/`** dentro de `ui-tests/booking-flow/` (no moverlos a la raíz del repo) — decisión deliberada para evitar hacks de `sys.path`.
- **El patrón `init.json` / `remote_config.json`** — no volver a mezclar lógica de entorno (`if os.environ.get("CI")`) dentro de la clase `Config`; ya se intentó y Andres lo corrigió explícitamente a favor de dos archivos de datos separados (mismo patrón que usa en su trabajo con Selenium).
- **El `continue-on-error: true` del step de booking flow en `tests.yml`** — no quitarlo asumiendo que "ya se arregló"; es una limitación externa confirmada (ver Restricciones/Reglas), no un parche temporal.
- **Los sufijos aleatorios en los identificadores de datos de test** (número de habitación, email) — no simplificar a valores 100% fijos; existen para evitar colisiones reales ya observadas contra la app compartida.
- **La versión fijada de `playwright` y el tag del `Dockerfile`** — no cambiar uno sin el otro (ver Reglas importantes, punto 4).
- **No agregar el trailer `Co-Authored-By: Claude`** a los commits de este repo, aunque sea el comportamiento por defecto en otros proyectos.

---

## Otras instrucciones permanentes

- Este repo es la implementación de las **semanas 4-7** de un plan de estudio de 14 semanas más amplio (Claude IA + QE Automation). El contexto de quién es Andres, su nivel, y las reglas de evaluación semanal viven en la memoria de Claude Code, no en este repo — si retomas este proyecto sin esa memoria, no asumas el rol de "profesor de plan de estudio" solo a partir de este archivo.
- Antes de escribir un locator o asumir un status code/comportamiento "correcto", **verificar contra la app/API real** (DevTools, `curl`, Postman, aria snapshot) en vez de adivinar por convención — la mayoría de los hallazgos documentados en los README de cada suite existen porque algo no se comportaba como "debería".
- Cada entregable nuevo debe quedar documentado en el `README.md` de su propia carpeta (no solo en el código) — es una regla del plan de estudio que este repo ya sigue en todas sus suites.
