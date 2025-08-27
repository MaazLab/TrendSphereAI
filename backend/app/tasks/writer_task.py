# backend/app/tasks/writer_task.py

from __future__ import annotations
from crewai import Task, Agent
from services.sanitize import sanitize

def create_write_task(agent: Agent, tone: str = 'professional') -> Task:
    """
    Task description for the Writer Agent, now includes tone and summarization.
    """
    description = (
        f"You will receive a research brief on {{topic}} for {{platform}}.\n"
        "Your task is to generate:\n"
        "1) A short, catchy {platform} post with 1 hook, 3-5 bullet points, and 1 CTA.\n"
        "2) A long-form LinkedIn article: Include a headline, intro, body, and conclusion.\n"
        "Ensure the tone is {tone}.\n"
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


def summarize_content(content: str, max_len: int = 4000) -> str:
    """
    Summarize the research content to make it concise and easy for post generation.
    """
    prompt = f"Summarize the following research content for social media: {content}"
    response = agent.llm.call(prompt=prompt)
    summarized_content = sanitize(response)[:max_len]
    return summarized_content
