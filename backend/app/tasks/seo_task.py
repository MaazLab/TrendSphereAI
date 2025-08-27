# backend/app/tasks/seo_task.py

from crewai import Task
from tools.keywords import keyword_suggest_tool
from tools.hashtags import hashtag_suggest_tool

def create_seo_task(agent):
    """
    Inputs expected at kickoff:
      - topic: str
      - platform: str
      - tone: str
      - content: str  (should contain the writer/editor output with SHORT_POST and LONG_DRAFT)
    """
    return Task(
        description=(
            "You are an SEO Optimization Agent for social media.\n"
            "Platform: {platform}\n"
            "Topic: {topic}\n"
            "Desired tone: {tone}\n\n"
            "Content to optimize (between tags):\n"
            "<content>\n{content}\n</content>\n\n"
            "Do the following:\n"
            "1) Extract 15–25 keywords/keyphrases from the content and topic using the keyword tool.\n"
            "2) Pick 8–12 primary keywords. Mark 3–5 of them as FOCUS KEYWORDS.\n"
            "3) Generate platform-appropriate hashtags grouped as Primary/Niche/Broad using the hashtag tool.\n"
            "4) Lightly revise the SHORT_POST to include 1–2 FOCUS KEYWORDS and 3–5 hashtags; preserve meaning and formatting; do not exceed platform norms.\n"
            "5) Lightly adjust the LONG_DRAFT headline/intro to include 1–2 FOCUS KEYWORDS, keeping tone and structure.\n"
            "6) Do not invent facts. Keep changes minimal and geared toward visibility/engagement.\n\n"
            "Output strictly in this format:\n"
            "KEYWORDS:\n- <keyword> (score: <num>) ... (8–12 items; indicate [FOCUS] on 3–5)\n\n"
            "HASHTAGS:\n- Primary: <#Tag1> <#Tag2> ...\n- Niche: <#Tag...>\n- Broad: <#Tag...>\n- All: <#Tag #Tag ...>\n\n"
            "OPTIMIZED_SHORT_POST:\n<text>\n\n"
            "OPTIMIZED_LONG_DRAFT:\n<text>\n\n"
            "NOTES:\n- <what changed and why>\n- <hashtag count & placement>\n"
        ),
        expected_output=(
            "KEYWORDS:\n- ...\n\nHASHTAGS:\n- Primary: ...\n- Niche: ...\n- Broad: ...\n- All: ...\n\n"
            "OPTIMIZED_SHORT_POST:\n...\n\nOPTIMIZED_LONG_DRAFT:\n...\n\nNOTES:\n- ...\n"
        ),
        agent=agent,
        tools=[keyword_suggest_tool(), hashtag_suggest_tool()],
        max_iter=3,
    )
