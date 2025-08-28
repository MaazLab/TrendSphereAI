# backend/app/agents/seo_agent.py

from crewai import Agent
from crewai.llm import LLM

def create_seo_agent(model: str | None = None, verbose: bool = True):
    return Agent(
        role="SEO Optimization Specialist",
        goal=(
            "Increase discoverability and engagement by optimizing keyword usage and hashtags "
            "for {platform} content about {topic}."
        ),
        backstory=(
            "You specialize in social SEO and growth. You identify high-intent keywords and "
            "craft platform-appropriate hashtag sets. You lightly weave focus keywords into "
            "copy without changing meaning or tone."
        ),
        llm=LLM(model=model) if model else None,
        verbose=verbose,
        allow_delegation=False,
    )
