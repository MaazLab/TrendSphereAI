import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import logging

logger = logging.getLogger(__name__)

# Pydantic schema for Grammar Check arguments
class GrammarCheckArgs(BaseModel):
    text: str = Field(..., description="Search query or question") # The text to check for grammar issues


class grammar_check_tool(BaseTool):
    """
    This tool checks the grammar of the input text.
    """
    
    name: str = "grammar_check_tool"
    description: str = (
        "Tool Name: grammar_check_tool\n"
        "Tool Arguments: {'text': {'description': 'Input text to check', 'type': 'str'}}\n"
        "Tool Description: Checks and fixes common grammar/spelling/punctuation issues. "
        "Uses language_tool_python if available; otherwise applies lightweight fixes."
    )
    args_schema: type[BaseModel] = GrammarCheckArgs

    def _run(self, text: str) -> str:
        url = "https://api.languagetool.org/v2/check"
        params = {
            'text': text,
            'language': 'en-US',
        }
        
        response = requests.post(url, data=params)
        result = response.json()
        
        # Get corrected text after grammar check
        corrected_text = result.get('matches', [])
        if corrected_text:
            corrected_text = " ".join([match['replacements'][0]['value'] for match in corrected_text])
            return corrected_text
        else:
            return text
        