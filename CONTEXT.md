# CONTEXT.md — qa-automation-portfolio

> Documento de continuidad para retomar este proyecto en cualquier sesión nueva de Claude Code sin perder contexto. Generado el 2026-09-18 verificando el estado real de los archivos (no solo la memoria de la conversación).
>
> Este repo es **parte** de un plan de estudio de 14 semanas más amplio (Claude IA + QE Automation). El plan completo vive en `C:\Users\andre\Documents\proyecto_claude\plan-estudio-andres-qe-ia-contexto-v2.md` y en la memoria de Claude Code (`plan_estudio_qe.md`, `perfil_andres.md`, `reglas_evaluacion.md`, `feedback_no_coauthor_portfolio.md`). Este CONTEXT.md documenta específicamente el estado del **repo**, no el plan de estudio completo.

---

## 1. OBJETIVO DEL PROYECTO

**Qué estamos construyendo:** `qa-automation-portfolio`, un repositorio público de GitHub que sirve como **portafolio de automatización QA** de Andres Gonzalez (QE en FLYR), pensado para adjuntarse en CV/LinkedIn y sostenerse en entrevistas técnicas.

**Objetivo final:** demostrar, con código real y funcionando, un stack alineado a lo que pide el mercado de QA Automation/SDET en 2026:

- UI testing (Playwright + Python)
- API testing (pytest + requests)
- CI/CD (GitHub Actions)
- Contenedores (Docker)
- BDD (pytest-bdd / Gherkin)

Todo contra **aplicaciones públicas de práctica** (nunca contra el entorno de trabajo real de Andres en FLYR — ver sección 5, "Separación público/privado").

Cada bloque de este repo corresponde a una semana del plan de estudio (semanas 4-7), y cada entregable debe poder explicarse en entrevista con la estructura *Qué / Por qué (evidencia de mercado) / Entregable*.

**URL pública:** https://github.com/anfelgonta201514/qa-automation-portfolio (repo público, sin trailer `Co-Authored-By` en los commits — ver sección 5).

---

## 2. ESTADO ACTUAL

### ✅ Qué está implementado y funciona

| Bloque | Estado | Evidencia |
|---|---|---|
| **UI — Booking flow** | ✅ Funciona local, **falla 100% en CI** (no bloqueante, ver sección 6) | `ui-tests/booking-flow/tests/booking/test_booking.py` |
| **UI — Admin** (login, navegación, creación de habitación) | ✅ Funciona, bloqueante en CI | `ui-tests/booking-flow/tests/admin/test_admin_options.py` |
| **UI — Batería: creación de habitaciones (`test_room_battery.py`)** | ✅ Funciona, bloqueante en CI | `ui-tests/booking-flow/tests/battery/test_room_battery.py` |
| **UI — Batería: flujo de reserva (`test_booking_battery.py`)** | ✅ Funciona local, agrupada con el booking flow en CI (no bloqueante, misma flakiness) | `ui-tests/booking-flow/tests/battery/test_booking_battery.py` |
| **UI — BDD** | ✅ Funciona, **NO conectado a CI todavía** | `ui-tests/booking-flow/features/` + `tests/bdd/` |
| **API testing** | ✅ Funciona (10/10 tests pasan) | `api-tests/restful-booker/` |
| **CI/CD (GitHub Actions)** | ✅ Funciona, badge verde | `.github/workflows/tests.yml` |
| **Docker** | ✅ Funciona local y en CI (mismo Dockerfile, "dos usos") | `Dockerfile`, `.dockerignore` |
| **Reportes Allure** | ✅ Funciona, con capturas de pantalla en puntos de validación | `utils/allure_helpers.py` |

Todo el trabajo está **commiteado y pusheado** a `origin/master`. Último commit: `ff834d4` — "Week 7 complete BDD implementation, improve allure reports, change pytest configuration". Working tree limpio (`git status` sin cambios pendientes al momento de escribir esto).

### ❌ Qué NO funciona / está incompleto

- **El flujo de booking falla el 100% de las veces al correr desde GitHub Actions** (no localmente) — afecta tanto a `tests/booking/test_booking.py` como a `tests/battery/test_booking_battery.py` (agrupados en el mismo step de CI). Es una limitación externa (ver sección 6), mitigada con `continue-on-error: true` — no bloquea el build, pero el step en sí sigue en rojo cada vez.
- **`tests/bdd/` no está conectado al workflow de CI** — el `.github/workflows/tests.yml` solo corre `tests/admin`, `tests/battery`, `tests/booking`. Los escenarios BDD solo se ejecutan localmente hasta ahora.
- **Casos negativos explícitos pendientes en UI**: teléfono inválido (se descubrió la regla — 10 dígitos falla, 11 pasa — pero no hay un test que lo verifique explícitamente) y login de admin con credenciales incorrectas.
- **`BasePage.accept_cookies_if_present()`** (en `pages/base_page.py`) es un método stub sin implementar (`# TODO: mapear el banner de cookies real...`) y no se usa en ningún lado actualmente.
- **No hay capturas de Allure en los tests de `api-tests/`** — el patrón de `attach_screenshot()` solo existe en el lado de UI (no aplica igual para API, pero tampoco hay nada equivalente ahí, ej. adjuntar el JSON de respuesta).
- **Semanas 8-14 del plan de estudio no han empezado** (servidor Oracle Cloud, backend Flask+Postgres, frontend, Routines, Cowork/MCP, demos IA, lanzamiento) — este repo (`qa-automation-portfolio`) es semanas 4-7 únicamente.

---

## 3. ARQUITECTURA

### Estructura real del repo (verificada, sin carpetas ignoradas)

```
qa-automation-portfolio/
├── .dockerignore
├── .github/
│   └── workflows/
│       └── tests.yml                    # CI/CD — ver sección 4
├── .gitignore
├── CONTEXT.md                            # este archivo
├── Dockerfile                            # imagen única, usada local y en CI
├── README.md                             # README raíz del portafolio
├── requirements.txt                      # dependencias Python (único archivo para todo el repo)
│
├── api-tests/restful-booker/             # Suite de API testing (semana 5)
│   ├── README.md
│   ├── conftest.py                       # fixtures: api_client, auth_token, booking_payload, created_booking
│   ├── pytest.ini
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_booking_crud.py
│   │   └── test_negative_cases.py
│   └── utils/
│       ├── booking_client.py             # BookingClient — wrapper de requests, rol de "Page Object" para HTTP
│       ├── config.py                     # BASE_URL, credenciales admin
│       └── schemas.py                    # modelos pydantic para validar shape de respuestas
│
└── ui-tests/booking-flow/                # Suite de UI testing (semanas 4, 6, 7)
    ├── README.md
    ├── config/
    │   ├── init.json                     # config para uso LOCAL
    │   └── remote_config.json            # config para PIPELINE/CI (headless forzado)
    ├── conftest.py                       # fixtures Playwright: browser/context/page/pages + trazas en fallo
    ├── data/
    │   ├── booking_battery.xlsx          # escenarios de batería del flujo de reserva
    │   └── room_battery.xlsx             # escenarios de batería de creación de habitaciones
    ├── features/                         # BDD (Gherkin) — vive AQUÍ, no en la raíz (ver sección 5)
    │   ├── admin_room.feature
    │   └── booking.feature
    ├── pages/                            # Page Object Model
    │   ├── admin_page.py
    │   ├── base_page.py
    │   ├── booking_page.py
    │   └── home_page.py
    ├── pytest.ini                        # incluye la config de plugins Allure (ver sección 5)
    ├── tests/
    │   ├── admin/test_admin_options.py
    │   ├── battery/
    │   │   ├── test_booking_battery.py
    │   │   └── test_room_battery.py
    │   ├── bdd/                          # step definitions que conectan .feature con Page Objects
    │   │   ├── test_admin_room_steps.py
    │   │   └── test_booking_steps.py
    │   └── booking/test_booking.py
    └── utils/
        ├── allure_helpers.py             # attach_screenshot() — helper compartido
        ├── battery_loader.py             # lee .xlsx con pandas → list[dict] para parametrize
        └── config.py                     # clase Config: elige init.json o remote_config.json según entorno
```

### Componentes principales y cómo se relacionan

1. **`Config` (un `utils/config.py` por suite, UI y API por separado)** — punto único de configuración. En UI, decide entre `init.json` (local) y `remote_config.json` (CI) según la variable de entorno `CI` (que GitHub Actions define automáticamente). El navegador (`BROWSER`) se sobreescribe puntualmente por variable de entorno porque la matrix de CI necesita 3 navegadores en la misma corrida.

2. **Page Object Model (UI)** — `BasePage` → `HomePage` / `BookingPage` / `AdminPage`. Cada uno encapsula locators + acciones de una pantalla. El fixture `pages` en `conftest.py` los instancia todos juntos por test.

3. **`BookingClient` (API)** — mismo rol que un Page Object, pero para HTTP: encapsula cada endpoint de Restful-booker como un método (`create_booking`, `get_booking`, `update_booking`, etc.), para que los tests no arme URLs/headers a mano.

4. **BDD (`features/` + `tests/bdd/`)** — capa adicional sobre el mismo POM, NO un framework paralelo. Los `.feature` describen escenarios en Gherkin (Given/When/Then); los step definitions en `tests/bdd/*.py` traducen cada línea a llamadas de los mismos Page Objects que ya usan los tests "planos". `pytest_bdd.scenarios(...)` genera automáticamente una función `test_...` por cada `Scenario` del `.feature`.

5. **Batería de datos (TR/battery)** — `battery_loader.load_battery()` lee un `.xlsx` con pandas y devuelve `list[dict]`; se usa con `@pytest.mark.parametrize` para generar un test por fila del Excel, sin duplicar código.

6. **Docker** — una sola imagen (`mcr.microsoft.com/playwright/python:v1.62.0-noble` como base) que sirve tanto para correr local (`docker run`) como dentro del workflow de CI (`docker/build-push-action`). Ver sección 5 para el porqué de la versión exacta.

7. **CI (`tests.yml`)** — dos jobs paralelos (`api-tests`, `ui-tests` en matrix de navegadores), cada uno construye/usa la misma imagen Docker y extrae resultados de Allure vía volúmenes montados.

---

## 4. ARCHIVOS IMPORTANTES

| Archivo | Qué hace | Nota |
|---|---|---|
| `Dockerfile` | Imagen única para local y CI | Tag de la imagen base **debe coincidir exacto** con la versión de `playwright` en `requirements.txt` |
| `requirements.txt` | Todas las dependencias Python del repo (UI + API) | `playwright==1.62.0` está **fijado**, no con `>=` (a propósito, ver sección 5) |
| `.github/workflows/tests.yml` | Pipeline de CI | Ver detalle completo en sección 3; nota clave: los dos steps de UI pasan `-p allure_pytest` explícito |
| `ui-tests/booking-flow/pytest.ini` | Config de pytest para la suite de UI | Tiene bloques **comentados** para activar reportes Allure puntualmente (ver sección 5) |
| `ui-tests/booking-flow/conftest.py` | Fixtures Playwright | `pages` fixture instancia `HomePage`, `BookingPage`, `AdminPage` juntos |
| `ui-tests/booking-flow/utils/config.py` | Elige `init.json` vs `remote_config.json` según `CI` env var | Patrón traído del trabajo de Andres en Selenium |
| `ui-tests/booking-flow/pages/admin_page.py` | Page Object del panel de Admin | Tiene `amenity_checkboxes` (dict) + `check_amenity()`/`uncheck_amenity()` genéricos, en vez de un método por checkbox |
| `ui-tests/booking-flow/utils/allure_helpers.py` | `attach_screenshot(page, name)` | Usar SOLO en puntos de validación (`Then`/asserts), no en cada acción |
| `ui-tests/booking-flow/utils/battery_loader.py` | Carga `.xlsx` → `list[dict]` | Acepta `dtype` explícito por columna (necesario para `phone`, que pandas infiere como número) |
| `ui-tests/booking-flow/features/*.feature` | Escenarios Gherkin | Solo 2 archivos, 1 escenario cada uno — cubren "el flujo de portada", no negativos |
| `api-tests/restful-booker/utils/booking_client.py` | Cliente HTTP para Restful-booker | `update_booking()` acepta `token` opcional para testear "sin cookie" como caso propio |
| `api-tests/restful-booker/utils/schemas.py` | Modelos pydantic | Valida shape de la respuesta de `POST /booking` |

### Cambios importantes realizados (cronológicos, resumen)

1. Scaffold inicial del repo, framework Playwright migrado del proyecto privado de Selenium (semana 4)
2. Page Objects construidos contra Restful Booker Platform + patrón TR/battery con Excel
3. Suite de API testing desde cero (Andres entró sin experiencia previa en pytest+requests)
4. CI/CD con GitHub Actions, matrix cross-browser
5. Descubrimiento de que el booking flow falla solo desde CI (no localmente) → `continue-on-error`
6. Migración de CI para usar Docker en vez de instalar Python/Playwright nativo en el runner
7. Fix de versión: `playwright==1.62.0` exacto + imagen `v1.62.0-noble` (antes desalineados)
8. BDD agregado con `pytest-bdd`, reutilizando los Page Objects existentes
9. Capturas de pantalla en Allure en puntos de validación (`attach_screenshot`)
10. Resolución del conflicto `allure-pytest` vs `allure-pytest-bdd` (ver sección 6) — el cambio más grande de la última sesión

---

## 5. DECISIONES TOMADAS

### `features/` vive dentro de `ui-tests/booking-flow/`, no en la raíz del repo
El plan original ponía `features/` como carpeta hermana en la raíz. Se decidió meterla dentro de `ui-tests/booking-flow/` para que los step definitions importen los Page Objects directamente, sin hacks de `sys.path` entre carpetas. Alternativa descartada: `features/` en la raíz + manipular `sys.path` en un `conftest.py` — más frágil y menos legible para un recruiter.

### `playwright==1.62.0` fijado exacto, no `>=1.45`
El tag de la imagen base de Docker (`mcr.microsoft.com/playwright/python:vX.Y.Z-noble`) debe coincidir EXACTO con la versión del paquete `playwright` instalado, o Playwright rechaza lanzar el navegador (error explícito de la propia librería). Con un rango abierto (`>=1.45`), un `pip install` futuro podría traer una versión más nueva y romper todo silenciosamente en el próximo build de Docker.

### `config/init.json` (local) + `config/remote_config.json` (CI), no una sola clase `Config` con lógica de entorno embebida
Enfoque inicial de Claude fue una sola clase `Config` que decidía `headless_mode` con un `if os.environ.get("CI")` inline. **Andres corrigió esto** señalando que en su trabajo (Selenium) usan dos archivos de config separados — mantiene la configuración como datos puros, no mezclada con lógica de entorno en el código. Se adoptó ese patrón.

### Docker se integró al CI (no se dejó solo como capacidad local)
El plan pedía explícitamente "un solo Dockerfile, dos usos" (local + pipeline). Se evaluó el trade-off (más complejidad/riesgo de debugging vs. fidelidad al plan) preguntando a Andres, quien eligió integrarlo completo. Se migró `tests.yml` de instalar Python/Playwright nativo a `docker build` + `docker run`, con caché de capas vía `type=gha` y resultados extraídos por volumen montado.

### Los commits del repo NO llevan `Co-Authored-By: Claude`
Andres notó que esa línea hacía aparecer a "Claude" en el listado de Contributors de GitHub y le preocupaba que pareciera que no escribió el código él. El autor real de cada commit siempre ha sido Andres (verificado con `git log --format=%an`). Se acordó que omitir esa línea es honesto siempre que Andres siga divulgando verbalmente el uso de Claude Code en entrevistas. Se reescribió el historial existente (`git filter-branch` + force-push) para quitarla de los primeros commits. **Regla dura de este repo** (no necesariamente de otros repos de Andres).

### Andres hace él mismo todo `git commit`/`git push`
Desde la semana de CI/CD en adelante, Andres pidió explícitamente NO delegar el commit/push a Claude — así puede revisar los cambios y preguntar con más facilidad antes de publicarlos. Claude prepara los cambios y avisa cuándo están listos para revisión.

### `allure-pytest` y `allure-pytest-bdd` desactivados por defecto, activados puntualmente
Ver detalle completo en la sección 6 (fue el problema más grande resuelto en la última sesión). Se decidió NO forzar un plugin fijo por defecto porque romper cualquiera de los dos casos de uso (tests planos vs. BDD) no era aceptable — se dejó como algo que el desarrollador activa a propósito según lo que necesite reportar.

### Separación estricta público/privado (regla del plan de estudio, no solo de este repo)
- **Portafolio público** (este repo): Restful Booker Platform (`automationintesting.online`) para UI, Restful-booker (`restful-booker.herokuapp.com`) para API.
- **Práctica privada de trabajo**: SunExpress UAT (repo separado, `playwright-XQ`, en TypeScript) — nunca se mezcla con este repo, por riesgo de NDA/confidencialidad con el empleador de Andres (FLYR).

### Números de habitación con sufijo aleatorio en la batería (no puramente aleatorios, no puramente fijos)
`room_battery.xlsx` usa números fijos (200-204) a propósito, para simular el patrón real de "TR con datos hardcodeados" de Selenium. Pero se le agrega un sufijo aleatorio de 2 dígitos al enviarlo, porque dos corridas de CI dentro de la ventana de reset de ~10 min de la app (frecuente durante desarrollo activo, disparando varios pushes seguidos) generaban colisiones de ID en el DOM. Se mantiene el número base del Excel para trazabilidad en el reporte.

---

## 6. PROBLEMAS Y SOLUCIONES

### Problema: el flujo de booking falla 100% de las veces desde GitHub Actions, nunca localmente
- **Qué se intentó primero:** `pytest-rerunfailures` (`--reruns 2 --reruns-delay 5`) asumiendo que era flakiness de red aleatoria.
- **Qué NO funcionó:** los reintentos fallaron igual las 3 veces, siempre en el mismo punto (justo después de confirmar la reserva), con el error nativo de Chrome `"This page couldn't load"` — señal de que no era aleatorio.
- **Diagnóstico confirmado:** se corrió el mismo test en local con `CI=true` (forzando headless, igual que el runner) y pasó siempre. Esto descartó que fuera un problema de headless o del código. La hipótesis más probable: `automationintesting.online` bloquea o limita tráfico desde rangos de IP de datacenter/nube (protección anti-bot común), algo fuera de nuestro control.
- **Qué funcionó:** separar ese step específico con `continue-on-error: true` en `tests.yml` — se ejecuta, se reporta, sube sus artifacts, pero no bloquea el build. Admin/Rooms siguen siendo bloqueantes porque nunca han fallado. Documentado explícitamente en ambos README (no oculto).

### Problema: mismatch de versión Playwright ↔ imagen Docker
- **Síntoma:** `BrowserType.launch: Executable doesn't exist...` con un mensaje de Playwright indicando exactamente qué tag de imagen se necesitaba.
- **Causa:** `requirements.txt` tenía `playwright>=1.45` (sin fijar), pip instaló 1.62.0, pero el Dockerfile decía `v1.61.0-noble`.
- **Solución:** fijar `playwright==1.62.0` exacto + actualizar el tag de la imagen a `v1.62.0-noble`. Sincronizado también el venv local a la misma versión.

### Problema: colisión de números de habitación fijos entre corridas de CI seguidas
- **Síntoma:** `strict mode violation: locator("#roomName200") resolved to 2 elements` — la app no valida IDs duplicados en su HTML.
- **Causa:** varios pushes de CI seguidos (debugueando) cayeron dentro de la misma ventana de reset de ~10 min de la app; el número fijo del Excel (200-204) ya existía de una corrida anterior.
- **Solución:** sufijo aleatorio de 2 dígitos agregado al número base del Excel (ver sección 5).

### Problema grande: `allure-pytest` y `allure-pytest-bdd` no pueden estar activos a la vez
- **Síntoma:** `ValueError: option names {'--alluredir'} already added` — pytest revienta al **cargar los plugins**, no solo al usar la opción.
- **Qué se intentó:** desactivar `allure-pytest` dejando solo `allure-pytest-bdd` activo (`-p no:allure_pytest` en `pytest.ini`).
- **Qué NO funcionó:** con solo `allure-pytest-bdd` activo, un `allure.attach()` dentro de un test **normal** (no BDD) como `test_admin_options.py` truena con `KeyError: None` — el listener de `allure-pytest-bdd` solo engancha eventos de `pytest_bdd` (confirmado leyendo su código fuente), nunca registra un "item" de Allure para tests planos.
- **Investigación:** se confirmó con búsqueda externa (GitHub issue oficial de `allure-framework/allure-python` #486, y un artículo técnico) que es una incompatibilidad **documentada y conocida** del ecosistema Allure, no un error de configuración propio.
- **Solución final:** desactivar AMBOS plugins por defecto en `pytest.ini` (`-p no:allure_pytest -p no:allure_pytest_bdd`), y reactivar el que corresponda explícitamente al pedir un reporte (`-p allure_pytest` o `-p allure_pytest_bdd`, nunca los dos juntos). CI actualizado para pasar `-p allure_pytest` explícito en sus dos steps de UI. `pytest.ini` local tiene dos bloques comentados (uno por tipo de reporte) para descomentar puntualmente — mismo patrón que Andres ya usa en su trabajo.

### Problema: `--clean-alluredir` en `addopts` rompía los runs sin plugin de Allure activo
- **Causa:** `--clean-alluredir` es una opción definida por los plugins de Allure; si ambos están desactivados por defecto, la opción ni siquiera existe, y pytest la rechaza como "unrecognized argument" en cualquier run normal.
- **Solución:** `--clean-alluredir` quedó SOLO documentado como parte de los comandos explícitos de reporte (README + bloques comentados en `pytest.ini`), nunca en el `addopts` activo por defecto.

### Problema de entorno: Docker Desktop no instalaba (WSL2 dañado)
- **Síntoma:** `REGDB_E_CLASSNOTREG` al correr `wsl --update`.
- **Solución:** se dejó que el propio `wsl` se autorreparara (prompt de "presiona cualquier tecla para reparar WSL"), luego `wsl --update` funcionó normal.

### Problema: screenshot de login en Allure mostraba el estado ANTES de loguearse
- **Causa:** la app es una SPA con transición client-side; `expect(Logout).to_be_visible()` confirma que el elemento nuevo apareció, pero no garantiza que el formulario viejo ya desapareció ni que terminó de cargar contenido async.
- **Solución:** se agregaron dos esperas adicionales antes de la captura: `expect(admin.admin_username_input).to_be_hidden()` (confirma que lo viejo se fue) y `expect(page.get_by_text("Loading...").first).to_be_hidden()` (confirma que terminó de cargar). El `.first` fue necesario porque "Loading..." aparece duplicado en el DOM (un `<span class="sr-only">` para lectores de pantalla + un `<p>` visible).

### Problema recurrente de entorno: Git Bash en Windows "traga" rutas estilo Unix
- Al verificar volúmenes de Docker con rutas como `/app/allure-results`, Git Bash (MSYS) las reinterpretaba como rutas de Windows, dando falsos negativos. **Solución:** usar PowerShell para esas verificaciones específicas, no Git Bash.

---

## 7. PENDIENTES

### Explícitamente pendientes (mencionados en README o en conversación)
- [ ] Conectar `tests/bdd/` al workflow de CI (`tests.yml`) — hoy solo corre local
- [ ] Caso negativo explícito: teléfono con longitud inválida (la regla ya se descubrió — 10 dígitos falla, 11 pasa — falta el test)
- [ ] Caso negativo explícito: login de admin con credenciales incorrectas
- [ ] Evaluar agregar `attach_screenshot()`-equivalente (adjuntar JSON de respuesta) a los tests de `api-tests/`

### Bugs conocidos / deuda técnica menor
- `pages/base_page.py::accept_cookies_if_present()` es un stub sin implementar ni usar — candidato a implementarlo o eliminarlo
- El README raíz todavía menciona una carpeta `reports/` en el diagrama de estructura que no existe como tal en el repo (Allure escribe a `allure-results/`, no a `reports/`)

### Mejoras pendientes (mencionadas como "para después", no bloqueantes)
- Publicar el reporte de Allure como GitHub Pages (el plan original lo daba como alternativa a "artifact del run", que ya está cubierto)
- Revisar si conviene agregar caché de pip además de la caché de capas Docker (impacto marginal, Docker ya cachea la capa de `pip install`)

### Fuera del alcance de este repo (pertenecen a semanas futuras del plan de estudio, no a `qa-automation-portfolio`)
- Semana 8: servidor Oracle Cloud (SSH, iptables, Nginx, Gunicorn, systemd)
- Semana 9: backend del portafolio web (PostgreSQL, Flask-SQLAlchemy, SSL)
- Semana 10: frontend + panel admin + **insertar en la BD todo lo documentado de este repo** (semanas 4-7)
- Semanas 11-14: Routines, Cowork/MCP, demos IA en vivo, lanzamiento

---

## 8. ÚLTIMO PUNTO DE TRABAJO

**Qué se estaba haciendo justo antes de crear este archivo:**

Se acababa de cerrar completamente la **semana 7** del plan de estudio (Docker + BDD), incluyendo una sesión larga de troubleshooting real sobre reportes de Allure:

1. Se agregó BDD (`pytest-bdd`) con dos features (`booking.feature`, `admin_room.feature`) y sus step definitions, reutilizando los Page Objects existentes.
2. Andres pidió capturas de pantalla en el reporte de Allure, pero **solo en puntos de validación**, no en cada acción — se creó `utils/allure_helpers.py::attach_screenshot()`.
3. Se descubrió que `allure-pytest` y `allure-pytest-bdd` no pueden convivir (conflicto de `--alluredir`), y que `allure-pytest-bdd` solo no sirve para tests planos. Se resolvió desactivando ambos por defecto en `pytest.ini` y documentando cómo reactivar cada uno puntualmente (incluyendo el patrón de bloques comentados que Andres ya usa en su trabajo).
4. Se corrigió CI (`tests.yml`) para pasar `-p allure_pytest` explícito en sus dos steps de UI, ya que dejaron de estar activos por defecto.
5. Todo esto se commiteó y pusheó por Andres (commit `ff834d4`).
6. Se hizo la evaluación de cierre de semana 7 (3/3 correctas).
7. Se le dio a Andres un resumen del estado completo del plan (semanas 1-7 completas, semana 8 en adelante pendiente).
8. **Este mismo mensaje** pidió crear este `CONTEXT.md`.

**Cuál debería ser el siguiente paso:**

Preguntarle a Andres si quiere:
- (a) Empezar la **semana 8** (servidor Oracle Cloud) — esto es un cambio de dominio grande, de QA automation a administración de servidor Linux/backend, y probablemente merece calibrar su experiencia previa en SSH/Linux/Nginx antes de empezar (mismo patrón usado en semanas anteriores: preguntar nivel antes de decidir cuánto explicar).
- (b) Cerrar algún pendiente de la sección 7 primero (conectar BDD a CI, casos negativos explícitos).
- (c) Pausar aquí — este repo (`qa-automation-portfolio`) ya cumple el hito de "repo completo según estándar de mercado 2026" que pedía el plan.

No hay ninguna tarea a medias ni ningún archivo sin commitear en este momento — es un punto de corte limpio.

---

## 9. COMANDOS IMPORTANTES

### Setup inicial (una sola vez)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium firefox webkit
```

### Correr tests — local, sin Docker
```bash
# API
cd api-tests/restful-booker
pytest -v

# UI — suite completa, sin reporte (rápido)
cd ui-tests/booking-flow
pytest -v

# UI — con reporte Allure (tests normales: admin, booking, batería)
pytest tests/admin tests/battery tests/booking -p allure_pytest --alluredir=allure-results --clean-alluredir

# UI — con reporte Allure BDD (agrega Given/When/Then al árbol de Allure)
pytest tests/bdd -p allure_pytest_bdd --alluredir=allure-results-bdd --clean-alluredir

# Ver un reporte generado
allure serve allure-results
```

⚠️ **Importante:** `allure-pytest` y `allure-pytest-bdd` NUNCA deben activarse juntos (ver sección 6). También, `pytest.ini` solo se detecta si el comando se corre desde `ui-tests/booking-flow/` (o con una ruta que lo tenga como ancestro) — correr desde la raíz del repo con una ruta que no exista ahí hace que pytest ignore ese `pytest.ini` silenciosamente.

Alternativa: en vez de escribir el comando completo, descomentar **un solo** bloque en `ui-tests/booking-flow/pytest.ini` (líneas 9-12 para reporte normal, o 13-16 para reporte BDD — nunca ambos a la vez) y correr `pytest -v` normal — volver a comentarlo después.

### Correr tests — con Docker (sin instalar nada más que Docker)
```bash
docker build -t qa-automation-portfolio .

# API
docker run --rm qa-automation-portfolio pytest api-tests/restful-booker -v

# UI (headless siempre, no hay pantalla en el contenedor)
docker run --rm -e CI=true qa-automation-portfolio pytest ui-tests/booking-flow -v
```

### Batería en paralelo
```bash
cd ui-tests/booking-flow
pytest tests/battery -v -n 4 -m room_battery -p allure_pytest --alluredir=allure-results --clean-alluredir
pytest tests/battery -v -n 4 -m booking_battery -p allure_pytest --alluredir=allure-results --clean-alluredir
```

### Git (Andres hace esto él mismo, no Claude — ver sección 5)
```bash
git add -A
git commit -m "mensaje sin trailer Co-Authored-By"
git push origin master
```

### CI
No requiere comando manual — se dispara en `push`/`pull_request` a `master`, o manualmente desde la pestaña **Actions → Tests → Run workflow** en GitHub (gracias a `workflow_dispatch`).

---

## 10. INFORMACIÓN QUE NO DEBE PERDERSE

- **Este repo es de PORTAFOLIO PÚBLICO.** Nunca debe contener URLs, selectores, código ni capturas del entorno de trabajo real de Andres (SunExpress UAT / FLYR). Esa práctica privada vive en un repo completamente distinto (`playwright-XQ`, TypeScript).

- **Los commits de este repo específico NO llevan `Co-Authored-By: Claude`** — regla explícita pedida por Andres, ya aplicada retroactivamente al historial. No agregar ese trailer aquí aunque sea el comportamiento por defecto en otros contextos.

- **Andres hace commit/push él mismo.** No commitear ni pushear a menos que lo pida explícitamente para un caso puntual — dejar los cambios listos y avisar.

- **`playwright==1.62.0` y el tag `v1.62.0-noble` del Dockerfile deben cambiar SIEMPRE juntos.** Si se actualiza uno sin el otro, los tests de UI en Docker fallan al lanzar el navegador (con un mensaje de error que además dice exactamente qué tag se necesita).

- **`allure-pytest` y `allure-pytest-bdd` son mutuamente excluyentes** — cualquier comando de pytest que los active a ambos simultáneamente revienta al cargar. Esto incluye no solo comandos explícitos sino también cualquier cosa que dependa de la auto-carga por defecto de plugins de pytest sin el `-p no:...` correspondiente.

- **El flujo de booking (`tests/booking/`, `tests/battery/test_booking_battery.py`) está marcado como no-bloqueante en CI a propósito** (`continue-on-error: true`). Un fallo ahí en el pipeline es esperado y no indica una regresión — solo revisar si además falla consistentemente en LOCAL, ese sí sería indicio real de un bug.

- **Este repo forma parte de un plan de estudio de 14 semanas más amplio.** El contexto completo de "quién es Andres, qué sabe, restricciones de tiempo, reglas de evaluación semanal" vive en la memoria de Claude Code (`~/.claude/projects/.../memory/`), no en este repo. Si se retoma este proyecto desde una sesión/máquina sin esa memoria, este `CONTEXT.md` cubre el estado técnico del repo, pero no el rol pedagógico "profesor/asistente de plan de estudio" que Claude ha estado cumpliendo en las últimas sesiones.

- **La app de práctica de UI (`automationintesting.online`) resetea sus datos cada ~10 minutos.** Cualquier test nuevo que se agregue debe seguir el mismo principio ya aplicado en todo el repo: crear sus propios datos con algún componente único (uuid, random), nunca asumir estado preexistente ni usar valores 100% fijos sin al menos un sufijo de unicidad.

- **Restful-booker (la API) tiene varias inconsistencias reales de status codes** (documentadas en `api-tests/restful-booker/README.md`) — no "corregirlas" asumiendo que son errores de test; son el comportamiento real y verificado de la API externa.
