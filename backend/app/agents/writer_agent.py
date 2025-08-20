from __future__ import annotations
from crewai import Agent, LLM
import os

def create_writer_agent(model: str | None = None, api_key: str | None = None, verbose: bool = True) -> Agent:
    # prefer env if not provided
    model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
    api_key = api_key or os.getenv("OPENAI_API_KEY")

    # Create LLM instance
    llm = LLM(model=model, api_key=api_key)

    backstory = (
        "You are a social media content writer. You convert research findings into posts that engage the audience. "
        "You adjust the tone based on the platform, and your writing should be clear, concise, and impactful. "
        "The goal is to craft posts and articles that will resonate with readers and prompt them to take action. "
        "Do not use emojis or the em dash character. Focus on persuasive and effective language."
    )

    return Agent(
        role="Content Writer",
        goal="Write a polished {platform} post and a longer LinkedIn draft about {topic} from the research brief.",
        backstory=backstory,
        allow_delegation=False,
        verbose=verbose,
        llm=llm,
    )
