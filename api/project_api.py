from typing import Any, Dict

from playwright.sync_api import APIRequestContext


class ProjectAPI:
    """
    API client for WorkFlow Pro project operations.

    Keeping API operations in a separate class allows
    the same methods to be reused by API and integration tests.
    """

    def __init__(
        self,
        request: APIRequestContext,
        base_url: str,
        token: str,
        tenant_id: str
    ):
        self.request = request
        self.base_url = base_url
        self.token = token
        self.tenant_id = tenant_id

    @property
    def headers(self) -> Dict[str, str]:
        """Return common API headers."""

        return {
            "Authorization": f"Bearer {self.token}",
            "X-Tenant-ID": self.tenant_id,
            "Content-Type": "application/json"
        }

    def create_project(
        self,
        name: str,
        description: str,
        team_members: list | None = None
    ) -> Dict[str, Any]:
        """
        Create a project through the API.

        Returns the JSON response from the API.
        """

        response = self.request.post(
            f"{self.base_url}/api/v1/projects",
            headers=self.headers,
            data={
                "name": name,
                "description": description,
                "team_members": team_members or []
            }
        )

        if not response.ok:
            raise AssertionError(
                "Project creation failed. "
                f"Status: {response.status}, "
                f"Response: {response.text()}"
            )

        response_data = response.json()

        assert "id" in response_data, (
            "API response does not contain project ID."
        )

        assert response_data["name"] == name, (
            "Created project name does not match "
            "the requested project name."
        )

        assert response_data["status"] == "active", (
            "New project is not in active status."
        )

        return response_data

    def delete_project(
        self,
        project_id: int
    ):
        """
        Delete a project created by the test.
        """

        response = self.request.delete(
            f"{self.base_url}/api/v1/projects/{project_id}",
            headers=self.headers
        )

        if not response.ok:
            raise AssertionError(
                "Project cleanup failed. "
                f"Status: {response.status}, "
                f"Response: {response.text()}"
            )
