from datetime import date, timedelta

from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.checkin_input = page.get_by_role("textbox").first
        self.checkout_input = page.get_by_role("textbox").nth(1)
        self.check_availability_button = page.get_by_role("button", name="Check Availability")

    def _gridcell_label(self, target_date: date) -> str:
        # El datepicker genera un aria-label tipo "Choose Friday, 10 July" para
        # cada celda visible. Se calcula a partir de una fecha real en vez de
        # hardcodear el texto, porque el string cambia todos los días.
        return f"Choose {target_date.strftime('%A')}, {target_date.day} {target_date.strftime('%B')}"

    def select_dates(self, nights_from_today: int = 1, stay_length: int = 4):
        checkin = date.today() + timedelta(days=nights_from_today)
        checkout = checkin + timedelta(days=stay_length)

        self.checkin_input.click()
        self.page.get_by_role("gridcell", name=self._gridcell_label(checkin)).click()

        self.checkout_input.click()
        self.page.get_by_role("gridcell", name=self._gridcell_label(checkout)).click()

        return checkin, checkout

    def search_availability(self):
        self.check_availability_button.click()

    def book_room(self, index: int = 1):
        # nth(index): la búsqueda puede devolver varias habitaciones disponibles.
        # index=0 toma la primera; se parametriza para poder elegir otra en tests futuros.
        self.page.get_by_role("link", name="Book now").nth(index).click()
