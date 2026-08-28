import random
import re

import allure

from utils.allure_helpers import attach_screenshot
from playwright.sync_api import expect


def test_admin_options(pages):
    home = pages["home"]
    admin = pages["admin"]
    room_number = str(random.randint(200, 9999))

    with allure.step("Login page"):
        home.goto()
        admin.goto_admin_login()
        admin.type_admin_username("admin")
        admin.type_admin_password("password")
        admin.click_admin_login_button()

        expect(admin.admin_rooms_option_button).to_be_visible()
        expect(admin.page.get_by_text("Loading...").first).to_be_hidden()
        attach_screenshot(admin.page, f"Login successful")

    with allure.step("Reports page"):
        admin.goto_admin_report()

        expect(admin.page).to_have_url(re.compile(r"admin/report"))
        expect(admin.page.get_by_text("Loading...").first).to_be_hidden()
        attach_screenshot(admin.page, f"Redirection successful")

    with allure.step("Rooms page"):
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
        attach_screenshot(admin.page, f"Room {room_number} created")