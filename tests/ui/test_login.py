import os

import pytest
from playwright.sync_api import Page, expect


BASE_URL = os.getenv(
    "BASE_URL",
    "https://app.workflowpro.com"
)


@pytest.mark.ui
def test_user_login(page: Page):
    """
    Verify that a valid user can log in successfully.

    The test uses Playwright's built-in waiting and
    assertions instead of fixed sleep delays.
    """

    # Navigate to login page
    page.goto(
        f"{BASE_URL}/login",
        wait_until="domcontentloaded"
    )

    # Verify login form is available
    expect(
        page.locator("#email")
    ).to_be_visible(timeout=15000)

    expect(
        page.locator("#password")
    ).to_be_visible(timeout=15000)

    # Fill login form
    page.locator("#email").fill(
        os.getenv(
            "COMPANY1_EMAIL",
            "admin@company1.com"
        )
    )

    page.locator("#password").fill(
        os.getenv(
            "COMPANY1_PASSWORD",
            "password123"
        )
    )

    # Submit login
    page.locator("#login-btn").click()

    # Wait for dashboard URL
    expect(page).to_have_url(
        lambda url: "/dashboard" in url,
        timeout=15000
    )

    # Verify dashboard loaded
    expect(
        page.locator(".welcome-message")
    ).to_be_visible(timeout=15000)


@pytest.mark.ui
def test_multi_tenant_access(page: Page):
    """
    Verify that a Company2 user only sees
    projects belonging to Company2.
    """

    page.goto(
        f"{BASE_URL}/login",
        wait_until="domcontentloaded"
    )

    # Wait for login form
    expect(
        page.locator("#email")
    ).to_be_visible(timeout=15000)

    # Login as Company2 user
    page.locator("#email").fill(
        os.getenv(
            "COMPANY2_EMAIL",
            "user@company2.com"
        )
    )

    page.locator("#password").fill(
        os.getenv(
            "COMPANY2_PASSWORD",
            "password123"
        )
    )

    page.locator("#login-btn").click()

    # Wait for dashboard
    expect(page).to_have_url(
        lambda url: "/dashboard" in url,
        timeout=15000
    )

    # Wait until project cards are available.
    # The application may load projects dynamically.
    project_cards = page.locator(
        ".project-card"
    )

    expect(
        project_cards.first
    ).to_be_visible(timeout=20000)

    # Validate tenant isolation
    count = project_cards.count()

    assert count > 0, (
        "No project cards were displayed "
        "for Company2."
    )

    for index in range(count):

        project_text = (
            project_cards.nth(index).text_content()
            or ""
        )

        assert "Company2" in project_text, (
            f"Tenant isolation issue: "
            f"project {index + 1} does not "
            f"belong to Company2."
        )
