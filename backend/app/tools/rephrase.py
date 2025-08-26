from openai import OpenAI
from crewai.tools import BaseTool
import os
import logging
from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)

client = OpenAI()

class RephraseArgs(BaseModel):
    text: str = Field(..., description="Input text to be rephrased")

# Pydantic schema for Rephrase arguments
class rephrase_tool(BaseTool):
    """
    Tool to rephrase text to improve vocabulary and style.
    """
    
    name: str = "rephrase_tool"
    description: str = (
        "Tool Name: rephrase_tool\n"
        "Tool Arguments: {'text': {'description': 'Input text to be rephrased', 'type': 'str'}}\n"
        "Tool Description: Rephrases text to improve clarity and tone with light synonym substitution."
    )
    args_schema: type[BaseModel] = RephraseArgs
    
    _map = {
        "very important": "crucial",
        "really important": "critical",
        "a lot of": "many",
        "make sure": "ensure",
        "help": "assist",
        "use": "leverage",
        "get": "obtain",
        "show": "demonstrate",
        "big": "significant",
    }
    
    def _run(self, text: str) -> str:
        out = text
        for k, v in self._map.items():
            out = out.replace(k, v)
            out = out.replace(k.capitalize(), v.capitalize())
        # tighten whitespace
        return "\n".join(line.strip() for line in out.splitlines())

