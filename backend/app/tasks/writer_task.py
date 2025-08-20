from __future__ import annotations
from crewai import Task, Agent

def create_write_task(agent: Agent, tone: str = 'professional') -> Task:
    description = (
        f"You will receive a research brief on {{topic}} for {{platform}}.\n"
        "Your task is to generate:\n"
        "1) A short, catchy {platform} post with 1 hook, 3-5 bullet points, and 1 CTA.\n"
        "2) A long-form LinkedIn article: Include a headline, intro, body, and conclusion.\n"
        f"Ensure the tone is {tone}.\n"
        "You will summarize lengthy content to make it concise and shareable."
    )

    expected_output = (
        "Two sections: SHORT_POST and LONG_DRAFT. Each is clean text ready to paste."
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )
