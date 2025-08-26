import os
from crews.social_article_crew import create_research_crew, create_writer_crew, create_editor_crew
from core.config import settings, ENV_PATH

# Ensure the TAVILY API key and OPENAI API key are available from the .env or environment variables
print("Loaded .env from:", ENV_PATH)
print("settings.openai_api_key set:", bool(settings.openai_api_key))
print("env OPENAI_API_KEY visible:", bool(os.getenv("OPENAI_API_KEY")))

# Set topic, platform and tone for testing
topic = "LLM privacy for developers"
platform = "LinkedIn"
tone = "professional"

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

# Run the test
if __name__ == "__main__":
    test_research_agent()
