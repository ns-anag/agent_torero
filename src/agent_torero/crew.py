"""
AgentTorero crew definition.
"""

from datetime import datetime
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.knowledge_config import KnowledgeConfig
from crewai.knowledge.source.text_file_knowledge_source import \
    TextFileKnowledgeSource
from crewai.project import CrewBase, agent, crew, task, tool

from src.agent_torero.config import get_config
from src.agent_torero.llm import GeminiFlashLLM, GeminiProLLM
from src.agent_torero.tools.github_tool import GithubPullRequestReviewTool
from src.agent_torero.tools.jira_tool import (JIRAAddCommentTool,
                                              JIRATicketInfoTool)
from src.agent_torero.tools.keywords import TestCaseSearchTool


@CrewBase
class AgentTorero:
    """AgentTorero crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    rbi_provider_knowledge = TextFileKnowledgeSource(
        file_paths=["rbi_provider_linux.txt"],
    )
    knowledge_config = KnowledgeConfig(results_limit=50, score_threshold=0.7)
    current_time = datetime.now().isoformat()

    @agent
    def github_specialist(self) -> Agent:
        """Creates the GitHub Specialist agent"""
        # pylint: disable=no-member
        return Agent(
            config=self.agents_config["github_specialist"],  # type: ignore[index]
            verbose=True,
            reasoning=True,
            llm=GeminiProLLM(),
        )

    @agent
    def jira_specialist(self) -> Agent:
        """Creates the JIRA Specialist agent"""
        # pylint: disable=no-member
        return Agent(
            config=self.agents_config["jira_specialist"],  # type: ignore[index]
            verbose=True,
            reasoning=True,
            llm=GeminiProLLM(),
            allow_delegation=False,
        )

    @agent
    def knowledge_retrieval_specialist(self) -> Agent:
        """Creates the Knowledge Retrieval Specialist Agent"""
        # pylint: disable=no-member
        return Agent(
            config=self.agents_config["knowledge_retrieval_specialist"],  # type: ignore[index]
            verbose=True,
            reasoning=True,
            knowledge_sources=[self.rbi_provider_knowledge],
            knowledge_config=self.knowledge_config,
            llm=GeminiProLLM(),
        )

    @agent
    def test_cases_retrieval_specialist(self) -> Agent:
        """Creates the Test Cases Retrieval Specialist Agent"""
        # pylint: disable=no-member
        return Agent(
            config=self.agents_config["test_cases_retrieval_specialist"],  # type: ignore[index]
            verbose=True,
            reasoning=True,
            llm=GeminiProLLM(),
        )

    @agent
    def reviewer_agent(self) -> Agent:
        """Creates the Reviewer Agent"""
        # pylint: disable=no-member
        return Agent(
            config=self.agents_config["reviewer_agent"],  # type: ignore[index]
            verbose=True,
            reasoning=True,
            max_reasoning_attempts=5,
            inject_date=True,
            llm=GeminiProLLM(),
        )

    @agent
    def jira_updater_agent(self) -> Agent:
        """Creates the JIRA Updater Agent"""
        # pylint: disable=no-member
        return Agent(
            config=self.agents_config["jira_updater_agent"],  # type: ignore[index]
            verbose=True,
            reasoning=False,
            inject_date=True,
            llm=GeminiFlashLLM(),
        )

    @task
    def github_pull_request_details_task(self) -> Task:
        """
        Task to fetch GitHub Pull Request details and diff.
        """
        # pylint: disable=no-member
        return Task(
            config=self.tasks_config["github_pull_request_details_task"],  # type: ignore[index]
        )

    @task
    def jira_tickets_info_task(self) -> Task:
        """
        Task to review GitHub PR code and extract Jira tickets.
        """
        # pylint: disable=no-member
        return Task(
            config=self.tasks_config["jira_tickets_info_task"],  # type: ignore[index]
        )

    @task
    def knowledge_retrieval_task(self) -> Task:
        """
        Task to retrieve the information from knowledge sources.
        """
        # pylint: disable=no-member
        return Task(
            config=self.tasks_config["knowledge_retrieval_task"],  # type: ignore[index]
        )

    @task
    def test_cases_retrieval_task(self) -> Task:
        """
        Task to retrieve relevant test cases from the test cases knowledge source.
        """
        # pylint: disable=no-member
        return Task(
            config=self.tasks_config["test_cases_retrieval_task"],  # type: ignore[index]
        )

    @task
    def review_and_synthesis_task(self) -> Task:
        """
        Task to synthesize GitHub PR and Jira ticket information.
        """
        # pylint: disable=no-member
        return Task(
            config=self.tasks_config["review_and_synthesis_task"],  # type: ignore[index]
            output_file="report.md",
        )

    @task
    def jira_add_comment_task(self) -> Task:
        """
        Task to add the review comment to a pre-configured Jira ticket.
        """
        # pylint: disable=no-member
        return Task(
            config=self.tasks_config["jira_add_comment_task"],  # type: ignore[index]
        )

    @tool
    def jira_ticket_info_tool(self) -> JIRATicketInfoTool:
        """Creates the JIRA Ticket Info tool"""
        return JIRATicketInfoTool()

    @tool
    def github_tool(self) -> GithubPullRequestReviewTool:
        """Creates the GitHub API tool"""
        return GithubPullRequestReviewTool()

    @tool
    def jira_add_comment_tool(self) -> JIRAAddCommentTool:
        """Creates the JIRA Add Comment tool"""
        return JIRAAddCommentTool()

    @tool
    def test_case_search_tool(self) -> TestCaseSearchTool:
        """Creates the Test Case Search tool"""
        return TestCaseSearchTool()

    @crew
    def crew(self) -> Crew:
        """Creates the AgentTorero crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=True,
            verbose=True,
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": get_config("GEMINI_API_KEY"),
                },
            },
            output_log_file=f"crew_ai_run_{self.current_time}.txt",
        )
