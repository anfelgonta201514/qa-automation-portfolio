import json
import os
from pathlib import Path

_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
# GitHub Actions define CI=true automáticamente en todos sus runners.
# Mismo patrón que en el proyecto de Selenium: init.json para local,
# remote_config.json para pipeline — dos archivos de datos, no lógica
# de entorno mezclada en la clase.
_CONFIG_FILE = "remote_config.json" if os.environ.get("CI") else "init.json"


class Config:
    with open(_CONFIG_DIR / _CONFIG_FILE, encoding="utf-8") as f:
        _data = json.load(f)

    BASE_URL = _data["BASE_URL"]
    HEADLESS_MODE = _data["headless_mode"]
    TAKE_SCREENSHOTS = _data["take_screenshots"]
    TAKE_LOGS = _data["take_logs"]
    DISABLE_COOKIES = _data["disable_cookies"]
    TEST_MODE = _data["test_mode"]
    # El "browser" de remote_config.json queda como default, pero la
    # matrix de CI necesita 3 navegadores distintos en la misma corrida
    # (un archivo estático no puede representar eso), así que aquí sí se
    # permite una sobreescritura puntual por variable de entorno.
    BROWSER = os.environ.get("BROWSER", _data["browser"])
    SLOW_MO = _data["slow_mo"]
