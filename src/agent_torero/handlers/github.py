"""GitHub handler for interacting with GitHub API.

This module provides functionality to fetch pull request details and diffs
from GitHub repositories using the GitHub REST API.
"""

import re
from typing import Optional

import requests

from src.agent_torero.config import get_config


class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class GitHubHandler:
    """Handler for GitHub operations.

    This class provides methods to interact with GitHub's REST API to fetch
    pull request information including details and diffs.
    """

    def __init__(self, pull_number: int, repo_name: str, owner: str = "netSkope"):
        """Initialize the GitHub handler.

        Args:
            pull_number: The pull request number to fetch.
            repo_name: The name of the GitHub repository.
            owner: The owner of the repository. Defaults to "netSkope".

        Raises:
            ValueError: If GITHUB_TOKEN is not found in environment variables.
        """
        self.pr_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls/{pull_number}"
        self.token = get_config("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN not found in environment variables.")

    def fetch_pr_details(self) -> dict:
        """Fetch pull request details from GitHub API.

        Returns:
            dict: JSON response containing pull request details if successful.
                  OR error information if the request fails.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        try:
            response = requests.get(self.pr_url, headers=headers, timeout=10)
            if response.status_code == 200:
                # Extract title and body
                pr_data = response.json()
                title = pr_data.get("title", "")
                body = pr_data.get("body", "")
                return {
                    "title": title,
                    "body": body,
                    "jira_tickets": self.extract_jira_tickets(title, body),
                }
            return {
                "error": f"Fetch PR details failed: {response.status_code}:{response.text[:200]}",
                "status_code": response.status_code,
            }
        except requests.RequestException as e:
            return {
                "error": f"Network error while fetching PR details: {str(e)}",
                "status_code": None,
            }
        except Exception as e:  # pylint: disable=broad-exception-caught
            return {
                "error": f"Unexpected error while fetching PR details: {str(e)}",
                "status_code": None,
            }

    def fetch_pr_diff(self) -> str:
        """Fetch pull request diff from GitHub API.

        Returns:
            str: The diff content in unified diff format if successful.

        Raises:
            GitHubAPIError: If the request fails or returns non-200 status.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3.diff",
        }
        try:
            response = requests.get(f"{self.pr_url}", headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            raise GitHubAPIError(
                f"Failed to fetch PR diff: {response.status_code} - {response.text[:200]}",
                status_code=response.status_code,
            )
        except requests.RequestException as e:
            raise GitHubAPIError("Network error while fetching PR diff") from e
        except Exception as e:  # pylint: disable=broad-exception-caught
            raise GitHubAPIError("Unexpected error while fetching PR diff") from e

    def extract_jira_tickets(self, title: str, body: str) -> list[str]:
        """Extract JIRA tickets from PR title and body

        Searches for RBI JIRA ticket patterns (e.g., RBI-1234) in the provided title and body.

        Args:
            title: The pull request title to search for JIRA tickets.
            body: The pull request body to search for JIRA tickets.

        Returns:
            list[str]: A list of JIRA ticket identifiers found in the title and body
        """
        pattern = r"\bRBI-\d+\b"
        tickets = re.findall(pattern, title)
        tickets.extend(re.findall(pattern, body))
        tickets = list(set(tickets))  # use set to avoid duplicates
        return tickets
