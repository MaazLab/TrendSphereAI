import os
from crews.social_article_crew import create_research_crew, create_writer_crew, create_editor_crew, create_seo_crew
from core.config import settings, ENV_PATH
import re

# Ensure the TAVILY API key and OPENAI API key are available from the .env or environment variables
print("Loaded .env from:", ENV_PATH)
print("settings.openai_api_key set:", bool(settings.openai_api_key))
print("env OPENAI_API_KEY visible:", bool(os.getenv("OPENAI_API_KEY")))

# Set topic, platform and tone for testing
topic = "LLM privacy for developers"
platform = "LinkedIn"
tone = "professional"


def _extract_cleaned_text(editor_result_str: str) -> str:
    """
    Try to extract the CLEANED section from the editor output.
    Falls back to the whole editor_result_str if pattern is not found.
    """
    # Matches: CLEANED:\n ... \nNOTES:
    m = re.search(r"CLEANED:\s*(.*?)\n\s*NOTES:", editor_result_str, flags=re.S | re.I)
    if m:
        cleaned = m.group(1).strip()
        # Remove wrapping fenced code block if present
        cleaned = re.sub(r"^```.*?\n|\n```$", "", cleaned, flags=re.S)
        return cleaned.strip()
    return editor_result_str.strip()


# Create the research crew and run the task
def test_research_agent():
    # Create research crew and execute
    research_crew = create_research_crew(model="gpt-4o-mini", verbose=True)
    inputs = {"topic": topic, "platform": platform}
    research_result = research_crew.kickoff(inputs=inputs)
    
    print(f"Research Result for '{topic}' on {platform}:")
    print(research_result)
    
    # Convert CrewOutput to a string (sanitize it)
    research_result_str = str(research_result)
    
    # Now, create the writer crew and pass the research result
    writer_crew = create_writer_crew(model="gpt-4o-mini", verbose=True)
    writer_inputs = {"topic": topic, "platform": platform, "research_result": research_result_str, "tone": tone}
    writer_result = writer_crew.kickoff(inputs=writer_inputs)
    
    print(f"\nWriter Result for '{topic}' on {platform}:")
    print(writer_result)
    
    # Convert CrewOutput to a string (sanitize it)
    writer_result_str = str(writer_result)
    
    # Now create the editor crew and pass the writer's result
    editor_crew = create_editor_crew(model="gpt-4o-mini", verbose=True)
    editor_inputs = {"content": writer_result_str, "platform": platform, "tone": tone}
    editor_result = editor_crew.kickoff(inputs=editor_inputs)
    
    print(f"\nEditor Result for '{topic}' on {platform}:")
    print(editor_result)
    
    editor_result_str = str(editor_result)
    cleaned_content = _extract_cleaned_text(editor_result_str)

    seo_crew = create_seo_crew(model="gpt-4o-mini", verbose=True)

    # Keep inputs simple & safe (only str/int/bool/list/dict). Extra keys are fine.
    # max_hashtags is a hint; your SEO task can ignore it if not used.
    # target_length: LinkedIn’s hard cap is 3,000 chars; we aim well below.
    seo_inputs = {
        "content": cleaned_content,
        "topic": topic,
        "platform": platform,
        "tone": tone,
        "max_hashtags": 12,
        "target_length": 1300,  # try to keep edited post comfortably under LinkedIn limits
        # you can add other knobs your SEO task supports (e.g., "include_emojis": True)
    }

    seo_result = seo_crew.kickoff(inputs=seo_inputs)

    print(f"\nSEO Result for '{topic}' on {platform}:")
    print(seo_result)

# Run the test
if __name__ == "__main__":
    test_research_agent()
