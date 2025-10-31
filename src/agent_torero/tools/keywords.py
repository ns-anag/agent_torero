"""
Tool to return keywords for test case search.
"""

from typing import List, Optional, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.agent_torero.handlers.keywords import SearchTestCases


class TestCaseSearchToolInput(BaseModel):
    """Input schema for TestCaseSearchTool."""

    keywords: Optional[List[str]] = Field(
        description=(
            "A list of keywords to filter test cases. "
            "If not provided, the tool will return a list of all available keywords."
        )
    )


class TestCaseSearchTool(BaseTool):
    """
    Tool for searching test cases by keywords.

    Also filters and retrieves test cases based on provided keywords.

    If no keywords are provided, it returns a list of all available keywords.

    """

    name: str = "Test Case Search Tool"
    description: str = (
        "Searches a CSV file for test cases. "
        "Can be used to get all keywords or to retrieve specific test cases "
        "based on a list of keywords. If no keywords are provided, "
        "it returns a list of all available keywords."
    )
    args_schema: Type[BaseModel] = TestCaseSearchToolInput

    # pylint: disable=arguments-differ
    def _run(self, keywords: Optional[List[str]] = None) -> str | List[str]:
        """
        Retrieves keywords or filters test cases based on provided keywords.
        If no keywords are provided, returns all available keywords. List[str].
        If keywords are provided, returns matching test cases. str.

        Args:
          keywords (Optional[List[str]]): List of keywords to filter test cases.
            If None, returns all available keywords.

        Returns:
          List[str]: List of all keywords from the knowledge base if no keywords are provided.

          List[str]: List of matching test cases if keywords are provided.
        """
        search_tool = SearchTestCases()
        response = []
        if keywords:
            # If keywords are provided return filtered test cases
            test_cases_list = search_tool.filter_by_keywords(keywords)
            # create a str like ID: <id>, Title: <title>, Summary: <summary>
            for test_case in test_cases_list:
                t = (
                    f"ID: {test_case.get('ID', 'N/A')}, Title: {test_case.get('Title', 'N/A')}, "
                    f"Summary: {test_case.get('Summary', 'N/A')}"
                )
                response.append(t)
            return response
        return search_tool.get_all_keywords()
