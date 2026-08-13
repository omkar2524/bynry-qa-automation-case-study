import os

import pytest
from playwright.sync_api import Page, expect


BASE_URL = os.getenv(
    "BASE_URL",
    "https://app.workflowpro.com"
)

COMPANY1_EMAIL = os.getenv(
    "COMPANY1_EMAIL",
    "admin@company1.com"
)

COMPANY1_PASSWORD = os.getenv(
    "COMPANY1_PASSWORD",
    "password123"
)


@pytest.mark.mobile
def test_project_access_on_mobile(page: Page):
    """
    Validate that a Company1 user can access the
    project dashboard from a mobile browser.

    This test is designed to run using a mobile
    browser/device configuration in BrowserStack.
    """

    # Open application
    page.goto(
        f"{BASE_URL}/login",
        wait_until="domcontentloaded"
    )

    # Verify login form
    expect(
        page.locator("#email")
    ).to_be_visible(timeout=15000)

    # Login
    page.locator("#email").fill(
        COMPANY1_EMAIL
    )

    page.locator("#password").fill(
        COMPANY1_PASSWORD
    )

    page.locator("#login-btn").click()

    # Verify dashboard
    expect(page).to_have_url(
        lambda url: "/dashboard" in url,
        timeout=15000
    )

    expect(
        page.locator(".welcome-message")
    ).to_be_visible(timeout=15000)

    # Verify projects are accessible
    project_cards = page.locator(
        ".project-card"
    )

    expect(
        project_cards.first
    ).to_be_visible(timeout=20000)

    # Verify that the project area is usable
    assert project_cards.count() > 0, (
        "No projects are displayed on mobile."
    )
