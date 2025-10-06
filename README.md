# AgentTorero Crew

Welcome to the AgentTorero Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Copy `.env.example` as `.env` and update values in  `.env` file**

- Modify `src/agent_torero/config/agents.yaml` to define your agents
- Modify `src/agent_torero/config/tasks.yaml` to define your tasks
- Modify `src/agent_torero/crew.py` to add your own logic, tools and specific args
- Modify `src/agent_torero/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the agent_torero Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The agent_torero Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Details

1.  RBI provider code base is cleand and added to knowledge/rbi_provider_linux.txt
2.  A csv format test cases from RBI Provider suite is cleaned up, adding SearchKeywords using gemini AI.
3.  created all_keywords.txt using set of SearchKeywords
