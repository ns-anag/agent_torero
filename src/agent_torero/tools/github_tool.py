"""
Crew AI GitHub Tool
"""

from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.agent_torero.handlers.github import GitHubAPIError, GitHubHandler


class GitHubPRReviewToolInput(BaseModel):
    """Input schema for GitHubPRReviewTool."""

    pull_number: int = Field(..., description="The Pull Request number.")
    repo_name: str = Field(..., description="The repository name.")


class GithubPullRequestReviewTool(BaseTool):
    """GitHub Pull Request Review Tool."""

    name: str = "GitHub Pull Request Review Tool"
    description: str = (
        "A tool to fetch GitHub Pull Request information for a PR Number and Repo "
        "Returns a dictionary containing PR details and diff."
    )
    args_schema: Type[BaseModel] = GitHubPRReviewToolInput

    # pylint: disable=arguments-differ
    def _run(self, pull_number: int, repo_name: str) -> dict:
        """Fetch GitHub Pull Request details and diff.
        Args:
            pull_number (int): The Pull Request number.
            repo_name (str): The repository name.
        Returns:
            dict: A dictionary containing PR details and diff or error information.
        """
        try:
            github_api = GitHubHandler(pull_number=pull_number, repo_name=repo_name)
            pr_details = github_api.fetch_pr_details()
            pr_diff = github_api.fetch_pr_diff()

            response_json = {
                "pr_details": pr_details,
                "pr_diff": pr_diff,
                "success": True,
            }
            return response_json

        except GitHubAPIError as e:
            # Return structured error information for the LLM
            return {
                "error": str(e),
                "status_code": getattr(e, "status_code", None),
                "success": False,
                "pr_details": None,
                "pr_diff": None,
            }
        except Exception as e:  # pylint: disable=broad-exception-caught
            return {
                "error": f"Unexpected error in GitHub tool: {str(e)}",
                "success": False,
                "pr_details": None,
                "pr_diff": None,
            }
