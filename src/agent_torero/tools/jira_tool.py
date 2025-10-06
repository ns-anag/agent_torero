"""
CrewAI JIRA tool for interacting with JIRA API

This module provides functions to interact with the JIRA API, including fetching
ticket details and comments.
"""

from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.agent_torero.handlers.jira import JIRAHandler


class JIRTicketInfoToolInput(BaseModel):
    """Input schema for JIRTicketInfoTool."""

    ticket_ids: list[str] = Field(
        ...,
        description=("A list of JIRA tickets identifiers " "e.g., ['RBI-1234', 'RBI-56789']."),
    )


class JIRATicketInfoTool(BaseTool):
    """
    JIRA Tool for fetching JIRA tickets details.

    """

    name: str = "JIRA Ticket Fetcher"
    description: str = (
        "Fetches and returns details of list of JIRA tickets "
        "including its summary, description, status, and comments. "
    )
    args_schema: Type[BaseModel] = JIRTicketInfoToolInput

    # pylint: disable=arguments-differ
    def _run(self, ticket_ids: list[str]) -> list[dict]:
        """Fetch details of multiple JIRA tickets.
        Args:
            ticket_ids: A list of JIRA ticket identifiers (e.g., ['RBI-1234', 'RBI-56789']).
        Returns:
            list[dict]: A list of dictionaries containing ticket details
                  (id, summary, description, status, list_of_comments)
                  or an error message if the ticket is not found {"error": <error_message>}.
        """
        jira_handler = JIRAHandler()
        tickets_details = jira_handler.fetch_tickets_details(ticket_ids)
        return tickets_details


class JIRAAddCommentToolInput(BaseModel):
    """Input schema for JIRAAddCommentTool."""

    comment: str = Field(
        ...,
        description="The comment text to add to the JIRA ticket.",
    )


class JIRAAddCommentTool(BaseTool):
    """
    JIRA Tool for adding comments to a JIRA ticket.
    Currently adds comment to a pre-configured ticket.

    """

    name: str = "JIRA Add Comment"
    description: str = (
        "Adds a comment to JIRA ticket. "
        "Useful for updating tickets with new information or feedback."
    )
    args_schema: Type[BaseModel] = JIRAAddCommentToolInput

    # pylint: disable=arguments-differ
    def _run(self, comment: str) -> bool:
        """
        Add a comment to a JIRA ticket.

        Args:
            comment: The comment text to add to the JIRA ticket.

        Returns:
            bool: True if the comment was added successfully, False otherwise.
        """
        jira_handler = JIRAHandler()
        success = jira_handler.add_comment_to_ticket(comment)
        return success
