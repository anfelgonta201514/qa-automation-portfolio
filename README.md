# qa-automation-portfolio

[![Tests](https://github.com/anfelgonta201514/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/anfelgonta201514/qa-automation-portfolio/actions/workflows/tests.yml)

Portafolio público de QA Automation — Andres Gonzalez.

Demuestra un stack alineado a mercado 2026: UI testing (Playwright), API testing (pytest + requests), CI/CD (GitHub Actions), contenedores (Docker) y BDD (pytest-bdd), todo contra aplicaciones públicas de práctica (no datos ni entornos de ningún empleador).

## Estructura

```
qa-automation-portfolio/
├── ui-tests/booking-flow/   → Playwright contra Restful Booker Platform (automationintesting.online)
│   ├── features/            → BDD (Gherkin) — vive aquí, no como carpeta separada,
│   │                           para reutilizar los Page Objects sin hacks de sys.path
│   └── tests/bdd/            → step definitions que conectan cada .feature con los Page Objects
├── api-tests/restful-booker/→ pytest + requests contra restful-booker.herokuapp.com
├── Dockerfile                → mismo usado en local y en CI
├── .github/workflows/       → CI
└── reports/                 → configuración/salida de Allure
```

## Stack

- Python 3.13, Playwright, pytest
- pytest-bdd para BDD (Gherkin)
- Allure para reportes
- GitHub Actions para CI
- Docker para entorno reproducible

## CI/CD (`.github/workflows/tests.yml`)

- Se dispara en `push`/`pull_request` a `master`, y también manualmente desde la pestaña Actions (`workflow_dispatch`)
- **Un solo `Dockerfile`, dos usos:** el mismo que corres en tu máquina (`docker build` + `docker run`) es el que se construye y corre dentro del workflow — nada de Python/Playwright instalado nativo en el runner, garantiza paridad exacta entre local y CI
- Caché de capas de Docker vía el backend de GitHub Actions (`cache-from`/`cache-to: type=gha`) para que los builds siguientes sean rápidos
- Job `api-tests` (rápido, sin navegador) + job `ui-tests` en matrix cross-browser (Chromium, Firefox, WebKit), corriendo en paralelo, cada uno con su propio `docker run` y resultados extraídos del contenedor vía volumen montado
- `config/remote_config.json` separa la config de pipeline de la de uso local (`init.json`) — mismo patrón que en Selenium: headless forzado y sin lógica de entorno mezclada en la clase `Config`
- El job de UI corre en dos steps: `admin + rooms` (bloqueante) y `booking flow` (`continue-on-error: true` + `--reruns 2`) — el flujo de booking falla consistentemente solo desde runners de GitHub, probablemente por bloqueo anti-bot del sitio de demo a IPs de datacenter (confirmado que no es un bug del código ni de Docker: el mismo test pasa siempre en local, headed o headless, dentro y fuera del contenedor). Se reporta y se guardan sus artifacts igual, pero no tumba el badge por una limitación de un tercero fuera de nuestro control. Detalle completo en `ui-tests/booking-flow/README.md`
- Resultados de Allure y trazas de fallos se suben como artifacts de cada run

## Cómo correr

**Con Docker (sin instalar nada más que Docker):**
```bash
docker build -t qa-automation-portfolio .

# API
docker run --rm qa-automation-portfolio pytest api-tests/restful-booker -v

# UI (headless siempre dentro del contenedor, no hay pantalla)
docker run --rm -e CI=true qa-automation-portfolio pytest ui-tests/booking-flow -v
```
El tag de la imagen base (`mcr.microsoft.com/playwright/python:vX.Y.Z-noble`) debe coincidir exacto con la versión de `playwright` fijada en `requirements.txt` — si se actualiza una, hay que actualizar la otra.

**Local (Python + venv):**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium firefox webkit
cd ui-tests/booking-flow
pytest
```

_(en progreso — ver estado en cada subcarpeta)_
