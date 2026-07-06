import json
from pathlib import Path

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "init.json"


class Config:
    with open(_CONFIG_PATH, encoding="utf-8") as f:
        _data = json.load(f)

    BASE_URL = _data["BASE_URL"]
    HEADLESS_MODE = _data["headless_mode"]
    TAKE_SCREENSHOTS = _data["take_screenshots"]
    TAKE_LOGS = _data["take_logs"]
    DISABLE_COOKIES = _data["disable_cookies"]
    TEST_MODE = _data["test_mode"]
    BROWSER = _data["browser"]
    SLOW_MO = _data["slow_mo"]
