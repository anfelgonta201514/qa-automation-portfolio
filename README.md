# qa-automation-portfolio

[![Tests](https://github.com/anfelgonta201514/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/anfelgonta201514/qa-automation-portfolio/actions/workflows/tests.yml)

Portafolio público de QA Automation — Andres Gonzalez.

Demuestra un stack alineado a mercado 2026: UI testing (Playwright), API testing (pytest + requests), CI/CD (GitHub Actions), contenedores (Docker) y BDD (pytest-bdd), todo contra aplicaciones públicas de práctica (no datos ni entornos de ningún empleador).

## Estructura

```
qa-automation-portfolio/
├── ui-tests/booking-flow/   → Playwright contra Restful Booker Platform (automationintesting.online)
├── api-tests/restful-booker/→ pytest + requests contra restful-booker.herokuapp.com
├── features/                → BDD con pytest-bdd
├── .github/workflows/       → CI
└── reports/                 → configuración/salida de Allure
```

## Stack

- Python 3.13, Playwright, pytest
- Allure para reportes
- GitHub Actions para CI
- Docker para entorno reproducible

## CI/CD (`.github/workflows/tests.yml`)

- Se dispara en `push`/`pull_request` a `master`, y también manualmente desde la pestaña Actions (`workflow_dispatch`)
- Job `api-tests` (rápido, sin navegador) + job `ui-tests` en matrix cross-browser (Chromium, Firefox, WebKit), corriendo en paralelo
- `config/remote_config.json` separa la config de pipeline de la de uso local (`init.json`) — mismo patrón que en Selenium: headless forzado y sin lógica de entorno mezclada en la clase `Config`
- Caché de dependencias pip y de los binarios de Playwright para acelerar corridas siguientes
- El job de UI corre en dos steps: `admin + rooms` (bloqueante) y `booking flow` (`continue-on-error: true` + `--reruns 2`) — el flujo de booking falla consistentemente solo desde runners de GitHub, probablemente por bloqueo anti-bot del sitio de demo a IPs de datacenter (confirmado que no es un bug del código: el mismo test pasa siempre en local, headed o headless). Se reporta y se guardan sus artifacts igual, pero no tumba el badge por una limitación de un tercero fuera de nuestro control. Detalle completo en `ui-tests/booking-flow/README.md`
- Resultados de Allure y trazas de fallos se suben como artifacts de cada run

## Cómo correr (ui-tests/booking-flow)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
cd ui-tests/booking-flow
pytest
```

_(en progreso — ver estado en cada subcarpeta)_
