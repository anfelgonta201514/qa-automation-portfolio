import pandas as pd
import pytest
from playwright.sync_api import expect

from utils.battery_loader import load_battery

# Se carga una sola vez, cuando pytest importa el archivo (no en cada test).
ROOM_SCENARIOS = load_battery("room_battery.xlsx")


@pytest.mark.parametrize(
    "scenario",
    ROOM_SCENARIOS,
    ids=[s["scenario_id"] for s in ROOM_SCENARIOS],
)
@pytest.mark.room_battery
def test_admin_room_battery(pages, scenario):
    home = pages["home"]
    admin = pages["admin"]

    home.goto()
    admin.goto_admin_login()
    admin.type_admin_username("admin")
    admin.type_admin_password("password")
    admin.click_admin_login_button()
    admin.goto_admin_rooms()

    room_number = str(scenario["room_number"])
    admin.type_admin_rooms_name(room_number)
    admin.select_admin_rooms_type(scenario["type"])
    admin.select_admin_rooms_accessible(scenario["accessible"])
    admin.type_admin_rooms_price(str(scenario["price"]))

    # Gotcha de pandas: una celda vacía en Excel ("twin_no_services") no se
    # lee como string vacío "", se lee como NaN (float). Si haces
    # scenario["services"].split(",") directo sobre un NaN, revienta.
    services = [] if pd.isna(scenario["services"]) else str(scenario["services"]).split(",")
    for service in services:
        admin.check_amenity(service)

    admin.click_admin_rooms_create()

    # id estable por fila (#roomName{numero}); más preciso que get_by_text,
    # que puede colisionar si el precio coincide con el número de habitación.
    expect(admin.page.locator(f"#roomName{room_number}")).to_be_visible()
