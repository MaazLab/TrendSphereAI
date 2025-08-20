from __future__ import annotations
from crewai import Agent, LLM
import os

def create_writer_agent(model: str | None = None, api_key: str | None = None, verbose: bool = True) -> Agent:
    # Get model from environment or use default
    model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
    api_key = api_key or os.getenv("OPENAI_API_KEY")

    llm = LLM(model=model, api_key=api_key)

    backstory = (
        "You are a content writer for social media platforms. "
        "You convert research findings into a post suitable for {platform}. "
        "Your writing style should match the tone of the platform and the user's preferences. "
        "Adjust tone to {tone} while respecting platform conventions. "
        "The goal is to engage the audience while being clear and concise."
    )

    return Agent(
        role="Content Writer",
        goal="Write a polished {platform} post and a longer LinkedIn draft about {topic} from the research brief.",
        backstory=backstory,
        allow_delegation=False,
        verbose=verbose,
        llm=llm,
    )
