from __future__ import annotations

import os
import logging
from typing import Optional
import requests
from pydantic import BaseModel, Field

from crewai.tools import BaseTool

logger = logging.getLogger(__name__)

TAVILY_URL = "https://api.tavily.com/search"


class WebSearchArgs(BaseModel):
    query: str = Field(..., description="Search query or question")
    max_results: int = Field(5, ge=1, le=10, description="Number of results to return")


class TavilyWebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Search the web for recent and relevant information about a topic. "
        "Returns a concise summary with links using the Tavily API."
    )
    args_schema: type[BaseModel] = WebSearchArgs

    def _run(self, query: str, max_results: int = 5) -> str:
        api_key: Optional[str] = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Web search not available. TAVILY_API_KEY is missing."

        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": True,
            "include_images": False,
            "include_raw_content": False,
        }
        try:
            resp = requests.post(TAVILY_URL, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.exception("Tavily web search failed")
            return f"Web search failed: {e}"

        answer = data.get("answer") or ""
        results = data.get("results") or []
        lines = []
        if answer:
            lines.append(f"High level answer:\n{answer}\n")
        if results:
            lines.append("Top sources:")
            for r in results[:8]:
                title = r.get("title") or "Untitled"
                url = r.get("url") or ""
                snippet = (r.get("content") or "")[:280].strip().replace("\n", " ")
                lines.append(f"- {title} | {url}\n  Snippet: {snippet}")
        return "\n".join(lines).strip() or "No results."
