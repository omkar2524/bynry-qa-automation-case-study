import os
import time

import pytest
from playwright.sync_api import Playwright, Page, expect

from api.project_api import ProjectAPI
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


BASE_URL = os.getenv(
    "BASE_URL",
    "https://app.workflowpro.com"
)

COMPANY1_TOKEN = os.getenv(
    "COMPANY1_TOKEN",
    "test-token-company1"
)

COMPANY1_TENANT = "company1"

COMPANY1_EMAIL = os.getenv(
    "COMPANY1_EMAIL",
    "admin@company1.com"
)

COMPANY1_PASSWORD = os.getenv(
    "COMPANY1_PASSWORD",
    "password123"
)

COMPANY2_EMAIL = os.getenv(
    "COMPANY2_EMAIL",
    "user@company2.com"
)

COMPANY2_PASSWORD = os.getenv(
    "COMPANY2_PASSWORD",
    "password123"
)


@pytest.mark.integration
def test_project_creation_flow(
    page: Page,
    playwright: Playwright
):
    """
    End-to-end integration test.

    Flow:
    1. Create project using API
    2. Verify project in Company1 web UI
    3. Verify Company2 cannot see the project
    4. Clean up the created project

    Mobile validation is executed separately using
    BrowserStack with the same project test data.
    """

    project_name = (
        f"Integration Test Project {int(time.time())}"
    )

    request = playwright.request.new_context()

    project_api = ProjectAPI(
        request=request,
        base_url=BASE_URL,
        token=COMPANY1_TOKEN,
        tenant_id=COMPANY1_TENANT
    )

    project_id = None

    try:

        # ==============================================
        # STEP 1: Create project through API
        # ==============================================

        project = project_api.create_project(
            name=project_name,
            description=(
                "Project created for API/UI "
                "integration testing"
            )
        )

        project_id = project["id"]

        assert project["name"] == project_name
        assert project["status"] == "active"

        # ==============================================
        # STEP 2: Login as Company1 user
        # ==============================================

        login_page = LoginPage(page)

        login_page.open(BASE_URL)

        login_page.login(
            COMPANY1_EMAIL,
            COMPANY1_PASSWORD
        )

        login_page.verify_login_success()

        # ==============================================
        # STEP 3: Verify project in Company1 UI
        # ==============================================

        dashboard = DashboardPage(page)

        dashboard.verify_dashboard_loaded()

        dashboard.verify_project_visible(
            project_name
        )

        # ==============================================
        # STEP 4: Verify tenant isolation
        # ==============================================

        # Log out / navigate back to login.
        # The exact logout mechanism would depend
        # on the application's implementation.

        page.goto(
            f"{BASE_URL}/login",
            wait_until="domcontentloaded"
        )

        # Login as Company2 user
        login_page.login(
            COMPANY2_EMAIL,
            COMPANY2_PASSWORD
        )

        login_page.verify_login_success()

        dashboard.verify_dashboard_loaded()

        # Company2 must NOT see Company1's project.
        dashboard.verify_project_not_visible(
            project_name
        )

    finally:

        # ==============================================
        # STEP 5: Clean up test data
        # ==============================================

        if project_id is not None:
            project_api.delete_project(
                project_id
            )

        request.dispose()
