from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, path: str = "/"):
        self.page.goto(path)

    def accept_cookies_if_present(self):
        # TODO: mapear el banner de cookies real de automationintesting.online con DevTools
        pass
