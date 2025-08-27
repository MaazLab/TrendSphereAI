from __future__ import annotations
from crewai import Crew

from agents.research_agent import create_research_agent
from tasks.research_task import create_research_task

from agents.writer_agent import create_writer_agent
from tasks.writer_task import create_write_task

from agents.editor_agent import create_editor_agent 
from tasks.editor_task import create_editor_task

from agents.seo_agent import create_seo_agent 
from tasks.seo_task import create_seo_task

# Create the Research Crew
def create_research_crew(model: str | None = None, verbose: bool = True) -> Crew:
    print("FUNC: create_research_crew")
    agent = create_research_agent(model=model, verbose=verbose)
    print("DEBUG\t\t agent: ", agent)
    task = create_research_task(agent)
    print("DEBUG\t\t task: ", task)
    return Crew(agents=[agent], tasks=[task])

# Create the Writer Crew
def create_writer_crew(model: str | None = None, verbose: bool = True) -> Crew:
    print("FUNC: create_writer_crew")
    agent = create_writer_agent(model=model, verbose=verbose)
    print("DEBUG\t\t agent: ", agent)
    task = create_write_task(agent)
    print("DEBUG\t\t task: ", task)
    return Crew(agents=[agent], tasks=[task])

# Create the Editor Crew
def create_editor_crew(model: str | None = None, verbose: bool = True) -> Crew:
    print("FUNC: create_editor_crew")
    agent = create_editor_agent(model=model, verbose=verbose)
    print("DEBUG\t\t agent: ", agent)
    task = create_editor_task(agent)
    print("DEBUG\t\t task: ", task)
    return Crew(agents=[agent], tasks=[task])

# Create the SEO Crew
def create_seo_crew(model: str | None = None):
    seo_agent = create_seo_agent(model=model)
    seo_task = create_seo_task(seo_agent)
    return Crew(
        agents=[seo_agent],
        tasks=[seo_task],
        verbose=True,
    )

