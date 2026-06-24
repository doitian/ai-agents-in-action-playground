import os

from openai import AsyncOpenAI

from agents import set_tracing_disabled
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

set_tracing_disabled(True)

_client = AsyncOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"],
)

model = OpenAIChatCompletionsModel(
    model="glm-5.2",
    openai_client=_client,
)
