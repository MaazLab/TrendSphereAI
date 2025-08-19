from crewai import Agent, LLM
from core.config import settings
from tools.web_search import TavilyWebSearchTool
from tools.trends import GoogleTrendsTool
from tools.scraper import ScrapeUrlTool

def create_research_agent(model: str | None = None, verbose: bool = True) -> Agent:
    print("FUNC: create_research_agent")
    llm = LLM(model=(model or settings.llm_model), api_key=settings.openai_api_key)
    tools = [TavilyWebSearchTool(), GoogleTrendsTool(), ScrapeUrlTool()]
    return Agent(
        role="Researcher",
        goal="Create an actionable content plan and brief on {topic} for {platform} that is current and engaging.",
        backstory=("You are a content research specialist for social media. "
                   "You gather recent insights, trend signals, key facts, and audience pain points. "
                   "You prepare a crisp brief for a writer and tailor findings to the platform."),
        tools=tools,
        allow_delegation=False,
        verbose=verbose,
        llm=llm,
    )
