"""
Unit tests for the SearchTestCases class.
"""

import sys
from pathlib import Path

import pytest

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from agent_torero.config import get_config
# pylint: disable=wrong-import-position
from agent_torero.handlers.keywords import SearchTestCases


@pytest.fixture
def search_test_cases():
    """
    Fixture to initialize SearchTestCases instance.
    """
    return SearchTestCases()


# pylint: disable=redefined-outer-name
def test_get_all_keywords(search_test_cases):
    """
    Test retrieval of all keywords.
    """
    print("AGENT_TORERO_ROOT_DIR:", get_config("AGENT_TORERO_ROOT_DIR"))
    keywords = search_test_cases.get_all_keywords()
    assert isinstance(keywords, list)
    assert all(isinstance(kw, str) for kw in keywords)


# pylint: disable=redefined-outer-name
def test_filter_by_keywords(search_test_cases):
    """
    Test filtering of test cases by valid keywords.
    """
    keywords = ["3rd Party Auth Flow", "push_mode"]
    results = search_test_cases.filter_by_keywords(keywords)
    assert isinstance(results, list)
    assert all(isinstance(item, dict) for item in results)


# pylint: disable=redefined-outer-name
def test_filter_by_keywords_not_found(search_test_cases):
    """
    Test filtering of test cases by valid keywords.
    """
    keywords = ["Nonexistent Keyword"]
    results = search_test_cases.filter_by_keywords(keywords)
    assert isinstance(results, list)
    assert not results
