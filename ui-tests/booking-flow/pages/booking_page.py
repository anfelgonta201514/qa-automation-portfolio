from playwright.sync_api import Page

from pages.base_page import BasePage


class BookingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.reserve_now_button = page.get_by_role("button", name="Reserve Now")
        self.first_name_input = page.get_by_role("textbox", name="Firstname")
        self.last_name_input = page.get_by_role("textbox", name="Lastname")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.phone_input = page.get_by_role("textbox", name="Phone")
        self.return_home_button = page.get_by_role("link", name="Return home")

    def fill_first_name(self, name: str):
        self.first_name_input.click()
        self.first_name_input.fill(name)

    def fill_last_name(self, name: str):
        self.last_name_input.click()
        self.last_name_input.fill(name)

    def fill_email(self, email: str):
        self.email_input.click()
        self.email_input.fill(email)

    def fill_phone(self, phone: str):
        self.phone_input.click()
        self.phone_input.fill(phone)

    def click_reserve_now(self):
        self.reserve_now_button.click()

    def click_return_home(self):
        self.return_home_button.click()
