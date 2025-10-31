"""
Handler for keyword-based test case search.
"""

from pathlib import Path
from typing import List

import pandas as pd
import re

from src.agent_torero.config import get_config


# pylint: disable=too-few-public-methods
class SearchTestCases:
    """
    A class to search test cases based on keywords.
    """

    def __init__(self) -> None:
        """
        Initialize the SearchTestCases class by loading the test cases CSV file.
        """
        root_dir = Path(get_config("AGENT_TORERO_ROOT_DIR", "."))
        csv_path = root_dir / "knowledge" / "test_cases.csv"
        self.all_keywords_file_path = root_dir / "knowledge" / "all_keywords.txt"
        if not csv_path.exists():
            raise FileNotFoundError(
                f"The test cases CSV file was not found at: {csv_path}"
            )

        self._df = pd.read_csv(csv_path, sep=";", dtype=str)
        # Ensure 'SearchKeywords' column exists and handle potential NaN values
        if "SearchKeywords" not in self._df.columns:
            raise ValueError("CSV file must contain a 'SearchKeywords' column.")
        self._df["SearchKeywords"] = self._df["SearchKeywords"].fillna("").astype(str)
        print("Test Case Search Tool initialized successfully.")

    def get_all_keywords(self) -> List[str]:
        """
        Returns a list of all keywords from the knowledge base.

        Returns:
            List[str]: A sorted list of unique keywords.
        """
        with open(self.all_keywords_file_path, "r", encoding="utf-8") as f:
            contents = f.read()
        return [kw.strip() for kw in contents.split(",") if kw.strip()]

    def filter_by_keywords(self, keywords: List[str]) -> List[dict]:
        """
        Filters the test cases to find matching cases with any of the provided keywords.

        Args:
            keywords (List[str]): A list of keywords to search for.

        Returns:
            List[dict]: A list of dictionaries representing the matching test cases.
            If no keywords are provided, returns an empty list.
            If no matches are found, returns an empty list.

        """
        if not keywords:
            return []

        # Use re.escape to handle special characters in keywords and \b for whole-word matching.
        pattern = "|".join([r"\b" + re.escape(k.strip()) + r"\b" for k in keywords])

        mask = self._df["SearchKeywords"].str.contains(
            pattern, case=False, na=False, regex=True
        )
        filtered_df = self._df[mask]

        return filtered_df.to_dict(orient="records")
