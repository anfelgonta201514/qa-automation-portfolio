from playwright.sync_api import Page

from pages.base_page import BasePage


class AdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Login
        self.admin_username_input = page.get_by_role("textbox", name="Username")
        self.admin_password_input = page.get_by_role("textbox", name="Password")
        self.admin_login_button = page.get_by_role("button", name="Login")

        # Admin options
        self.admin_login_option_button = page.get_by_role("link", name="Admin", exact=True)
        self.admin_report_option_button = page.get_by_role("link", name="Report")
        self.admin_rooms_option_button = page.get_by_role("link", name="Rooms")
        self.admin_logout_option_button = page.get_by_role("button", name="Logout")

        # Create room
        self.admin_rooms_name_input = page.get_by_test_id("roomName")
        self.admin_rooms_type_dropdown = page.locator("#type")
        self.admin_rooms_accessible_dropdown = page.locator("#accessible")
        self.admin_rooms_price_input = page.locator("#roomPrice")
        self.admin_rooms_wifi_checkbox = page.get_by_role("checkbox", name="WiFi")
        self.admin_rooms_tv_checkbox = page.get_by_role("checkbox", name="TV")
        self.admin_rooms_views_checkbox = page.get_by_role("checkbox", name="Views")
        self.admin_rooms_radio_checkbox = page.get_by_role("checkbox", name="Radio")
        self.admin_rooms_refreshments_checkbox = page.get_by_role("checkbox", name="Refreshments")
        self.admin_rooms_safe_checkbox = page.get_by_role("checkbox", name="Safe")
        self.admin_rooms_create_button = page.get_by_role("button", name="Create")

    # Options interaction
    def goto_admin_login(self):
        self.admin_login_option_button.click()

    def goto_admin_report(self):
        self.admin_report_option_button.click()

    def goto_admin_rooms(self):
        self.admin_rooms_option_button.click()

    def click_admin_logout(self):
        self.admin_logout_option_button.click()

    # Login actions
    def type_admin_username(self, username: str):
        self.admin_username_input.fill(username)

    def type_admin_password(self, password: str):
        self.admin_password_input.fill(password)

    def click_admin_login_button(self):
        self.admin_login_button.click()

    # Create room actions
    def type_admin_rooms_name(self, rooms_name: str):
        self.admin_rooms_name_input.fill(rooms_name)

    def select_admin_rooms_type(self, room_type: str):
        self.admin_rooms_type_dropdown.select_option(room_type)

    def select_admin_rooms_accessible(self, option: str):
        self.admin_rooms_accessible_dropdown.select_option(option)

    def type_admin_rooms_price(self, price: str):
        self.admin_rooms_price_input.fill(price)

    def check_admin_rooms_wifi_checkbox(self):
        self.admin_rooms_wifi_checkbox.check()

    def check_admin_rooms_tv_checkbox(self):
        self.admin_rooms_tv_checkbox.check()

    def check_admin_rooms_views_checkbox(self):
        self.admin_rooms_views_checkbox.check()

    def check_admin_rooms_radio_checkbox(self):
        self.admin_rooms_radio_checkbox.check()

    def check_admin_rooms_refreshments_checkbox(self):
        self.admin_rooms_refreshments_checkbox.check()

    def check_admin_rooms_safe_checkbox(self):
        self.admin_rooms_safe_checkbox.check()

    def uncheck_admin_rooms_wifi_checkbox(self):
        self.admin_rooms_wifi_checkbox.uncheck()

    def uncheck_admin_rooms_tv_checkbox(self):
        self.admin_rooms_tv_checkbox.uncheck()

    def uncheck_admin_rooms_views_checkbox(self):
        self.admin_rooms_views_checkbox.uncheck()

    def uncheck_admin_rooms_radio_checkbox(self):
        self.admin_rooms_radio_checkbox.uncheck()

    def uncheck_admin_rooms_refreshments_checkbox(self):
        self.admin_rooms_refreshments_checkbox.uncheck()

    def uncheck_admin_rooms_safe_checkbox(self):
        self.admin_rooms_safe_checkbox.uncheck()

    def click_admin_rooms_create(self):
        self.admin_rooms_create_button.click()