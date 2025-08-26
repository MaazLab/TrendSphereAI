from crewai import Task
from tools.grammar_check import grammar_check_tool  # Grammar Checking Tool
from tools.rephrase import rephrase_tool  # Rephrasing Tool

def create_editor_task(agent):
    """
    Editor Task:
    - Receives {content} from the writer.
    - Runs grammar check.
    - Rephrases to match platform tone/constraints.
    - Returns final edited copy.
    """
    return Task(
        description="""You are an editor responsible for enhancing the quality of the content.
        Platform: {platform}.
        "Desired tone: {tone}"
        
        "Edit the text inside <content>...</content>:"
        "<content>
        {content}
        </content>"
        
        "Do the following:"
        1) Run a grammar check and fix errors.
        2) Rephrase for clarity, concision, and style using synonym substitution when it helps.
        3) Ensure it fits the platform norms (e.g., LinkedIn) and is easy to read.
        4) Preserve meaning; do not invent facts.
        Output two sections:
            - CLEANED: The final polished text ready to publish.
            - NOTES: Bullet list of the main edits (grammar/style/tone/length).
        """,
        expected_output=(
            "CLEANED:\n<final text>\n\n"
            "NOTES:\n- <edit 1>\n- <edit 2>\n..."
        ),
        agent=agent,
        tools=[grammar_check_tool(), rephrase_tool()],
        max_iter=3,  # Allow a maximum of 3 iterations for tool usage
    )
