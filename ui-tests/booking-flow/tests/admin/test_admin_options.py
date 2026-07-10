import random
import re

from playwright.sync_api import expect


def test_admin_options(pages):
    home = pages["home"]
    admin = pages["admin"]
    room_number = str(random.randint(200, 9999))

    home.goto()
    admin.goto_admin_login()
    admin.type_admin_username("admin")
    admin.type_admin_password("password")
    admin.click_admin_login_button()

    expect(admin.page.get_by_role("button", name="Logout")).to_be_visible()
    admin.goto_admin_report()
    expect(admin.page).to_have_url(re.compile(r"admin/report"))

    admin.goto_admin_rooms()
    expect(admin.page).to_have_url(re.compile(r"admin/rooms"))
    admin.type_admin_rooms_name(room_number)
    admin.select_admin_rooms_type("Single")
    admin.select_admin_rooms_accessible("true")
    admin.type_admin_rooms_price("111")
    admin.check_amenity("WiFi")
    admin.check_amenity("Safe")
    admin.click_admin_rooms_create()

    expect(admin.page.locator(f"#roomName{room_number}")).to_be_visible()