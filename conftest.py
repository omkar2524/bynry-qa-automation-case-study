import pytest
from playwright.sync_api import Page


@pytest.fixture
def page(page: Page):
    """
    Provides a fresh Playwright page for each test.

    pytest-playwright manages the browser lifecycle,
    while this fixture provides a clean page for tests.
    """

    page.set_default_timeout(15000)

    yield page
