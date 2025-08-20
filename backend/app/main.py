import os
from crews.social_article_crew import create_research_write_crew  # Importing the new combined crew
from core.config import settings, ENV_PATH

# Ensure the TAVILY API key and OpenAI key are available from the .env or environment variables
print("Loaded .env from:", ENV_PATH)
print("settings.openai_api_key set:", bool(settings.openai_api_key))
print("env OPENAI_API_KEY visible:", bool(os.getenv("OPENAI_API_KEY")))

# Set topic and platform for testing
topic = "LLM privacy for developers"
platform = "LinkedIn"

# Create the crew (Research + Writer) and run the task
def test_research_and_writer_agent():
    # Creating the crew that includes both Research and Writer agents
    crew = create_research_write_crew(model="gpt-4o-mini", verbose=True)
    inputs = {"topic": topic, "platform": platform}
    
    # Kick off the crew task (Research + Writer)
    result = crew.kickoff(inputs=inputs)
    
    # Print the final result
    print(f"\n===== Final Output for '{topic}' on {platform} =====")
    print(result)

# Run the test
if __name__ == "__main__":
    test_research_and_writer_agent()
