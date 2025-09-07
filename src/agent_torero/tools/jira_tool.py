"""
CrewAI JIRA tool for interacting with JIRA API

This module provides functions to interact with the JIRA API, including fetching
ticket details and comments.
"""

from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.agent_torero.handlers.jira import JIRAHandler


class JIRAToolInput(BaseModel):
    """Input schema for JIRATool."""

    ticket_ids: list[str] = Field(
        ...,
        description=("A list of JIRA tickets identifiers " "e.g., ['RBI-1234', 'RBI-56789']."),
    )


class JIRATool(BaseTool):
    """
    JIRA Tool for fetching JIRA tickets details.

    """

    name: str = "JIRA Ticket Fetcher"
    description: str = (
        "Fetches and returns details of list of JIRA tickets "
        "including its summary, description, status, and comments. "
    )
    args_schema: Type[BaseModel] = JIRAToolInput

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
