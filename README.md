# qa-automation-portfolio

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
