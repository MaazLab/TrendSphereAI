
from crewai import Agent
from tools.grammar_check import grammar_check_tool  # Grammar Checking Tool
from tools.rephrase import rephrase_tool  # Rephrasing Tool

def create_editor_agent(model: str | None = None, verbose: bool = True) -> Agent:
    """
    Creates the Editor Agent which checks for grammar and rephrases the text.
    """
    return Agent(
        role="Content Editor",
        goal="Edit and polish the article ensuring grammar, style, and tone are suitable for social media.",
        backstory="""You are an editor responsible for improving the content by checking for grammar mistakes,
                     rephrasing for style, and enhancing vocabulary to make the article suitable for LinkedIn.""",
        tools=[grammar_check_tool(), rephrase_tool()],
        verbose=verbose,
    )
