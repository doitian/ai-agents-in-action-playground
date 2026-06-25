import os
from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio, MCPServerStdioParams
import asyncio

from agent_config import model

SANDBOX = os.path.dirname(os.path.abspath(__file__))
MCP_SCRIPT = Path(__file__).with_name("mcp_research_tools.py").resolve()


async def main():
    research_agent = Agent(
        name="Research Agent",
        model=model,
        instructions="""
    You are a research assistant.
    Your role is to find research sources.
    Do not make up or invent any research sources.
    Always hand off to the thinking agent.
    """,
    )
    thinking_agent = Agent(
        name="Thinking Agent",
        model=model,
        instructions="""
    You are a research planning assistant.
    Your role is to plan the research.
    You will receive a list of research sources from the research agent.
    Use the sequentialThinking tool to create a research plan based on the sources.
    Always hand off to the filesystem agent.
    """,
    )
    filesystem_agent = Agent(
        name="Filesystem Agent",
        model=model,
        instructions="""
    You are a filesystem assistant.
    Your role is to write the output as a text file.
    Never make up or invent any output.
    """,
    )

    # Instantiate the servers next…
    servers = [
        MCPServerStdio(
            name="Research Tools",
            params=MCPServerStdioParams(
                command="mcp",
                args=["run", str(MCP_SCRIPT)],
            ),
        ),
        MCPServerStdio(
            name="sequential-thinking",
            params={
                "command": "bunx",
                "args": ["@modelcontextprotocol/server-sequential-thinking"],
            },
            client_session_timeout_seconds=300,
        ),
        MCPServerStdio(
            name="filesystem",
            params={
                "command": "bunx",
                "args": ["@modelcontextprotocol/server-filesystem", SANDBOX],
            },
            client_session_timeout_seconds=300,
        ),
    ]

    async with (
        servers[0] as research_srv,
        servers[1] as thinking_srv,
        servers[2] as fs_srv,
    ):
        goal = """
Produce a research plan to find the book 'The Hitchhiker's Guide to the Galaxy'
"""

        print("Running...", goal)
        research_agent.mcp_servers = [research_srv]
        research_agent.handoffs = [thinking_agent]
        thinking_agent.mcp_servers = [thinking_srv]
        thinking_agent.handoffs = [filesystem_agent]
        filesystem_agent.mcp_servers = [fs_srv]
        result = await Runner.run(research_agent, goal, max_turns=25)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
