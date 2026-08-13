from playwright.sync_api import Page, expect


class DashboardPage:
    """
    Page Object for the WorkFlow Pro dashboard.
    """

    def __init__(self, page: Page):
        self.page = page

        self.welcome_message = page.locator(
            ".welcome-message"
        )

        self.project_cards = page.locator(
            ".project-card"
        )

    def verify_dashboard_loaded(self):
        """
        Verify that the dashboard has loaded successfully.
        """

        expect(
            self.welcome_message
        ).to_be_visible(timeout=15000)

    def get_project_cards(self):
        """
        Return the project card locator.
        """

        expect(
            self.project_cards.first
        ).to_be_visible(timeout=20000)

        return self.project_cards

    def verify_project_visible(
        self,
        project_name: str
    ):
        """
        Verify that a specific project is visible.
        """

        project = self.project_cards.filter(
            has_text=project_name
        )

        expect(
            project
        ).to_be_visible(timeout=15000)

    def verify_project_not_visible(
        self,
        project_name: str
    ):
        """
        Verify that a specific project is not visible.
        """

        project = self.project_cards.filter(
            has_text=project_name
        )

        expect(
            project
        ).not_to_be_visible(timeout=5000)
