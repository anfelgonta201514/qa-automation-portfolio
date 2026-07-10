from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_battery(filename: str, dtype: dict | None = None) -> list[dict]:
    # dtype permite forzar columnas como texto (ej. teléfono): pandas infiere
    # tipo numérico en columnas que solo tienen dígitos, y eso rompe .fill()
    # de Playwright, que exige str.
    return pd.read_excel(DATA_DIR / filename, dtype=dtype).to_dict(orient="records")