from playwright.sync_api import Page, expect


class LoginPage:
    """
    Page Object for the WorkFlow Pro login page.

    Keeping selectors and login actions here makes
    the tests easier to maintain.
    """

    def __init__(self, page: Page):
        self.page = page

        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-btn")

    def open(self, base_url: str):
        """Open the login page."""
        self.page.goto(
            f"{base_url}/login",
            wait_until="domcontentloaded"
        )

    def login(self, email: str, password: str):
        """Log in using the supplied credentials."""

        expect(
            self.email_input
        ).to_be_visible(timeout=15000)

        self.email_input.fill(email)
        self.password_input.fill(password)

        self.login_button.click()

    def verify_login_success(self):
        """Verify that login redirected to the dashboard."""

        expect(
            self.page
        ).to_have_url(
            lambda url: "/dashboard" in url,
            timeout=15000
        )

        expect(
            self.page.locator(".welcome-message")
        ).to_be_visible(timeout=15000)
