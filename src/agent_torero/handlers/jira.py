"""
JIRA handler to interact with JIRA API

This module provides a JIRAHandler class that allows interaction with the JIRA API
to fetch issue details based on JIRA ticket identifiers.
"""

from typing import Optional

from atlassian import Jira

from src.agent_torero.config import get_config


class JIRAAPIError(Exception):
    """Custom exception for JIRA API errors."""

    def __init__(self, message: str, ticket_id: Optional[str] = None):
        super().__init__(message)
        self.ticket_id = ticket_id


class JIRAHandler:
    """Handler for JIRA operations.

    This class provides methods to interact with the JIRA API to fetch issue details.
    """

    def __init__(self):
        """Initialize the JIRA handler.

        Args:
            save_to_file: Whether to save ticket details to a file for debugging.

        Raises:
            ValueError: If any required JIRA environment variable is missing.
        """
        self.server: Optional[str] = get_config("JIRA_SERVER")
        self.user_email: Optional[str] = get_config("JIRA_USER_EMAIL")
        self.api_token: Optional[str] = get_config("JIRA_API_TOKEN")

        if not all([self.server, self.user_email, self.api_token]):
            raise ValueError("One or more JIRA environment variables are missing.")

        try:
            self.jira = Jira(
                url=self.server,  # type: ignore
                username=self.user_email,
                password=self.api_token,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            raise JIRAAPIError("Failed to initialize JIRA connection") from e

    def fetch_ticket_details(self, ticket_id: str) -> dict:
        """
        Fetch details of a single JIRA ticket.

        Args:
            ticket_id: A JIRA ticket identifier (e.g., 'RBI-1234').
        Returns:
            dict: A dictionary containing ticket details
                  (id, summary, description, status, list_of_comments)
                  or an error message if the ticket is not found {"error": <error_message>}.

        """
        if not ticket_id:
            error_msg = "No ticket ID provided."
            return {"error": error_msg}

        try:
            issue = self.jira.issue(ticket_id)
            comments = self.jira.issue_get_comments(ticket_id)

            # Extracting relevant fields - issue is already a dict with 'fields' key
            fields = issue.get("fields", {}) if isinstance(issue, dict) else {}
            status = fields.get("status", {}) if isinstance(fields.get("status"), dict) else {}

            # Handle comments safely
            safe_comments = comments if comments is not None else {}
            safe_comments = safe_comments.get("comments", [])

            ticket_info = {
                "id": ticket_id,
                "summary": fields.get("summary", "No summary available"),
                "description": fields.get("description", "No description available"),
                "status": status.get("name", "Unknown status"),
                "comments": [
                    comment.get("body", "")
                    for comment in safe_comments
                    if isinstance(comment, dict)
                ],
            }
            return ticket_info
        except Exception as e:  # pylint: disable=broad-exception-caught
            error_msg = f"Failed to fetch details for {ticket_id}: {str(e)}"
            return {"id": ticket_id, "error": error_msg}

    def fetch_tickets_details(self, ticket_ids: list[str]) -> list[dict]:
        """
        Fetch details of multiple JIRA tickets.

        Args:
            ticket_ids: A list of JIRA ticket identifiers (e.g., ['RBI-1234', 'RBI-5678']).
        Returns:
            list[dict]: A list of dictionaries containing ticket details or error messages.

        """
        if not ticket_ids:
            return [{"error": "No ticket IDs provided."}]

        results = []
        for ticket_id in ticket_ids:
            result = self.fetch_ticket_details(ticket_id)
            results.append(result)

        return results

    def add_comment_to_ticket(self, comment: str) -> bool:
        """
        Add a comment to a JIRA ticket.

        Args:
            comment(required): The comment text to add to the ticket.
        Returns:
            bool: True if the comment was added successfully, False otherwise.

        """
        ticket_id = "RBI-38719"  # Example ticket ID; replace with actual logic as needed

        try:
            self.jira.issue_add_comment(ticket_id, comment)
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Failed to add comment to {ticket_id}: {str(e)}")
            return False
