# backend/app/tasks/research_task.py
from __future__ import annotations

from crewai import Task, Agent


def create_research_task(agent: Agent) -> Task:
    """
    Task instructions for the research agent suitable for social media content.
    """
    print("FUNC: create_research_task")
    description = (
        "Research the topic: {topic} for the platform: {platform}.\n"
        "1) Use web_search to find recent insights, definitions, key facts, and opposing viewpoints.\n"
        "2) Use trend_insights to list up to 10 relevant keywords or queries. Prefer queries with higher values.\n"
        "3) If web_search returns interesting source links, use scrape_url on 1 to 3 of them to extract text for facts.\n"
        "4) Identify the target audience and their pain points. Include 2 to 4 concrete reader takeaways.\n"
        "5) Propose a structure for a short post and for a longer article. Each should include a hook, 3 to 5 bullet points, and a call to action tailored to {platform}.\n"
        "6) Suggest 8 to 12 SEO keywords and 5 to 10 platform suitable hashtags.\n"
        "7) Provide 3 example hooks and 3 CTA lines that fit the platform style guidelines."
    )

    expected_output = (
        "Return a content brief with the following sections:\n"
        "- Summary of current insights\n"
        "- Audience and pain points\n"
        "- Trend keywords list\n"
        "- Outline for short post\n"
        "- Outline for long article\n"
        "- Example hooks and CTAs\n"
        "- Suggested keywords and hashtags\n"
        "- Source links list\n"
        "Keep the brief concise and skimmable."
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )
