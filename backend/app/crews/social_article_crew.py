# backend/app/crews/social_article_crew.py
from __future__ import annotations

from crewai import Crew
from agents.research_agent import create_research_agent
from tasks.research_task import create_research_task


def create_research_crew(model: str | None = None, verbose: bool = True) -> Crew:
    print("FUNC: create_research_crew")
    agent = create_research_agent(model=model, verbose=verbose)
    print("DEBUG\t\t agent: ",agent)
    task = create_research_task(agent)
    print("DEBUG\t\t task: ",task)
    return Crew(agents=[agent], tasks=[task])
