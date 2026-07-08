import os

import pytest
from playwright.sync_api import sync_playwright

from pages.admin_page import AdminPage
from pages.booking_page import BookingPage
from pages.home_page import HomePage
from utils.config import Config

TRACES_DIR = os.path.join(os.path.dirname(__file__), "traces")


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, Config.BROWSER)
    browser = browser_type.launch(headless=Config.HEADLESS_MODE, slow_mo=Config.SLOW_MO)
    yield browser
    browser.close()


@pytest.fixture
def context(browser):
    context = browser.new_context(base_url=Config.BASE_URL)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.close()


@pytest.fixture
def page(context, request):
    page = context.new_page()
    yield page
    # El fixture `page` se destruye antes que `context` (orden inverso al de
    # creación), así que aquí es el único lugar donde se debe detener el
    # tracing: si se llamara tracing.stop() otra vez luego en `context`,
    # fallaría porque ya estaría detenido.
    if request.node.rep_call.failed:
        os.makedirs(TRACES_DIR, exist_ok=True)
        context.tracing.stop(path=os.path.join(TRACES_DIR, f"{request.node.name}.zip"))
        page.screenshot(path=os.path.join(TRACES_DIR, f"{request.node.name}.png"))
    else:
        context.tracing.stop()


@pytest.fixture
def pages(page):
    return {
        "home": HomePage(page),
        "booking": BookingPage(page),
        "admin": AdminPage(page),
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
