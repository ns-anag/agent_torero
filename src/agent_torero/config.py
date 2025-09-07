"""
Centralized configuration management for the application.

This module provides functions and configuration for managing environment variables
and application settings. It validates required variables and provides helpers for
retrieving configuration values in various types.
"""

import os
import sys
from typing import Any, Dict, Optional

import dotenv

# Load environment variables
dotenv.load_dotenv()

# Required environment variables
REQUIRED_VARS = {
    "GITHUB_TOKEN": "GitHub personal access token",
    "GEMINI_API_KEY": "Google Gemini API key",
    "JIRA_SERVER": "JIRA server URL",
    "JIRA_USER_EMAIL": "JIRA user email",
    "JIRA_API_TOKEN": "JIRA API token",
}

# Optional environment variables with defaults
OPTIONAL_VARS = {
    "OPENAI_API_KEY": "dummy",  # Dummy value to satisfy CrewAI validation
    "LOG_LEVEL": "INFO",
    "MAX_DIFF_SIZE": "50000",
    "SAVE_JIRA_DEBUG": "false",
}

# Validate and collect environment variables
CONFIG: Dict[str, Any] = {}


def validate_config() -> None:
    """
    Validate all required environment variables are present.

    Raises:
        SystemExit: If any required environment variable is missing.
    """
    missing_vars = []

    # Check for required environment variables
    for var_name, description in REQUIRED_VARS.items():
        value = os.getenv(var_name)
        if not value:
            missing_vars.append(f"{var_name} ({description})")
        CONFIG[var_name] = value

    # Add optional environment variables with defaults
    for var_name, default in OPTIONAL_VARS.items():
        CONFIG[var_name] = os.getenv(var_name, default)

    # Exit if required variables are missing
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        sys.exit(1)


def get_config(key: str, default: Optional[Any] = None) -> Any:
    """
    Get a configuration value safely with optional default.

    Args:
        key (str): The configuration key to retrieve.
        default (Optional[Any], optional): The default value if key is not found. Defaults to None.

    Returns:
        Any: The configuration value or the default.
    """
    return CONFIG.get(key, default)


def get_bool_config(key: str, default: bool = False) -> bool:
    """
    Get a boolean configuration value.

    Args:
        key (str): The configuration key to retrieve.
        default (bool, optional): The default boolean value if key is not found. Defaults to False.

    Returns:
        bool: The boolean configuration value.
    """
    value = get_config(key, str(default)).lower()
    return value in ("true", "1", "yes", "on")


def get_int_config(key: str, default: int = 0) -> int:
    """
    Get an integer configuration value.

    Args:
        key (str): The configuration key to retrieve.
        default (int, optional): The default integer value if key is not found or conversion fails. Defaults to 0.

    Returns:
        int: The integer configuration value.
    """
    try:
        return int(get_config(key, str(default)))
    except (ValueError, TypeError):
        return default


# Initialize configuration on import
validate_config()
