import os
import time

import pytest
from playwright.sync_api import Playwright

from api.project_api import ProjectAPI


BASE_URL = os.getenv(
    "BASE_URL",
    "https://app.workflowpro.com"
)

COMPANY1_TOKEN = os.getenv(
    "COMPANY1_TOKEN",
    "test-token-company1"
)

COMPANY1_TENANT = "company1"


@pytest.mark.api
def test_create_project_via_api(
    playwright: Playwright
):
    """
    Verify that a project can be created successfully
    through the WorkFlow Pro API.
    """

    project_name = (
        f"API Automation Project {int(time.time())}"
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
        # Create project
        project = project_api.create_project(
            name=project_name,
            description="Project created by API automation test"
        )

        project_id = project["id"]

        # Validate response
        assert project["name"] == project_name
        assert project["status"] == "active"

    finally:
        # Clean up test data
        if project_id is not None:
            project_api.delete_project(project_id)

        request.dispose()
