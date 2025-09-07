"""
AgentTorero crew definition.
"""
import os
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.text_file_knowledge_source import \
    TextFileKnowledgeSource
from crewai.project import CrewBase, agent, crew, task, tool

from src.agent_torero.tools.jira_tool import JIRATool
from src.agent_torero.config import get_config


@CrewBase
class AgentTorero:
    """AgentTorero crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    rbi_provider_knowledge = TextFileKnowledgeSource(
        file_paths=["rbi_provider_linux.txt"],
    )

    @agent
    def jira_specialist(self) -> Agent:
        """Creates the JIRA Specialist agent"""
        # pylint: disable=no-member
        return Agent(
            config=self.agents_config["jira_specialist"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def reviewer_agent(self) -> Agent:
        """Creates the Reviewer Agent"""
        # pylint: disable=no-member
        return Agent(
            config=self.agents_config["reviewer_agent"],  # type: ignore[index]
            verbose=True,
            reasoning=True,
            max_reasoning_attempts=3,
            knowledge_sources=[self.rbi_provider_knowledge],
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
    def review_jira_impact_task(self) -> Task:
        """
        Task to review Jira tickets and provide impact analysis.
        """
        # pylint: disable=no-member
        return Task(
            config=self.tasks_config["review_jira_impact_task"],  # type: ignore[index]
            output_file="report.md",
        )

    @tool
    def jira_ticket_info_tool(self) -> JIRATool:
        """Creates the JIRA Ticket Info tool"""
        return JIRATool()

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
                    "model": "models/embedding-001",
                    "api_key": get_config("GEMINI_API_KEY"),
                },
            },
        )

