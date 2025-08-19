import os
from crews.social_article_crew import create_research_crew
from core.config import settings, ENV_PATH

# Ensure the TAVILY API key is available from the .env or environment variables
# assert settings.tavily_api_key, "TAVILY_API_KEY is not set. Please check your .env or environment."
print("Loaded .env from:", ENV_PATH)
print("settings.openai_api_key set:", bool(settings.openai_api_key))
print("env OPENAI_API_KEY visible:", bool(os.getenv("OPENAI_API_KEY")))


# Set topic and platform for testing
topic = "LLM privacy for developers"
platform = "LinkedIn"

# Create the crew and run the task
def test_research_agent():
    crew = create_research_crew(model="gpt-4o-mini", verbose=True)
    inputs = {"topic": topic, "platform": platform}
    
    # Kick off the research task and get the result
    result = crew.kickoff(inputs=inputs)
    
    # Print the result
    print(f"Research Result for '{topic}' on {platform}:")
    print(result)

# Run the test
if __name__ == "__main__":
    test_research_agent()
