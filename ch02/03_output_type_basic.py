from agents import Agent, Runner
from pydantic import BaseModel

from agent_config import model

instructions = """
You are a research planning assistant.

**TASK INSTRUCTIONS**
- You will be given a research topic.
- Your task is to provide a plan on how to research this topic.
- Output 5 concise tasks (5 words or less) to your plan.
"""


class ResearchPlanModel(BaseModel):
    tasks: list[str]
    """A list of tasks to perform for research."""


agent = Agent(
    name="Research Planner",
    instructions=instructions,
    output_type=ResearchPlanModel,
    model=model,
)

input = "learn about AI agents"

result = Runner.run_sync(
    agent,
    input=input,
)

print(result.final_output)
