# backend/app/crews/social_article_crew.py
from __future__ import annotations

from crewai import Crew
from agents.research_agent import create_research_agent
from tasks.research_task import create_research_task
from agents.writer_agent import create_writer_agent
from tasks.writer_task import create_write_task


def create_research_crew(model: str | None = None, verbose: bool = True) -> Crew:
    print("FUNC: create_research_crew")
    agent = create_research_agent(model=model, verbose=verbose)
    print("DEBUG\t\t agent: ",agent)
    task = create_research_task(agent)
    print("DEBUG\t\t task: ",task)
    return Crew(agents=[agent], tasks=[task])

def create_write_crew(model: str | None = None, verbose: bool = True) -> Crew:
    researcher = create_research_agent(model=model, verbose=verbose)
    writer = create_writer_agent(model=model, verbose=verbose)

    # Define tasks for both agents
    research_task = create_research_task(researcher)
    write_task = create_write_task(writer)

    # Research and Writer agents interact sequentially in the Crew
    return Crew(agents=[researcher, writer], tasks=[research_task, write_task])
