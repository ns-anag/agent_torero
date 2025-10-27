"""
This module sets up the Gemini LLM using the crewai library.
"""

from typing import Any

from crewai import LLM

from src.agent_torero.config import get_config

gemini_api_key = get_config("GEMINI_API_KEY")


# pylint: disable=too-few-public-methods
class GeminiProLLM:
    """
    Singleton class that returns high reasoning 2.5 Pro Gemini LLM instance
    """

    gemini_pro_llm: LLM = None  # type: ignore

    # pylint: disable=unused-argument
    def __new__(cls, *args: Any, **kwds: Any) -> LLM:
        """
        Create a new instance of the GeminiProLLM class if it doesn't exist.
        """
        if cls.gemini_pro_llm is None:
            if not gemini_api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set.")
            cls.gemini_pro_llm = LLM(
                model="gemini/gemini-2.5-pro",
                api_key=gemini_api_key,
                reasoning_effort="high",
                temperature=0.0,  # Lower temperature for more consistent results.
                # stream=True,
                max_retries=6,
            )
        return cls.gemini_pro_llm


class GeminiFlashLLM:
    """
    Singleton class that returns medium reasoning 2.5 Flash Gemini LLM instance
    """

    gemini_flash_llm: LLM = None  # type: ignore

    # pylint: disable=unused-argument
    def __new__(cls, *args: Any, **kwds: Any) -> LLM:
        """
        Create a new instance of the GeminiFlashLLM class if it doesn't exist.
        """
        if cls.gemini_flash_llm is None:
            if not gemini_api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set.")
            cls.gemini_flash_llm = LLM(
                model="gemini/gemini-2.5-flash",
                api_key=gemini_api_key,
                reasoning_effort="medium",
                temperature=0.0,  # Lower temperature for more consistent results.
                # stream=True,
                max_retries=6,
            )
        return cls.gemini_flash_llm
