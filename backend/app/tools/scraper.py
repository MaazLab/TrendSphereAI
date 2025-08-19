from __future__ import annotations

import logging
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from crewai.tools import BaseTool

logger = logging.getLogger(__name__)


class ScrapeArgs(BaseModel):
    url: str = Field(..., description="Fully qualified URL to scrape")
    max_chars: int = Field(4000, ge=500, le=16000, description="Max characters to return")


class ScrapeUrlTool(BaseTool):
    name: str = "scrape_url"
    description: str = "Fetch a web page and return cleaned readable text to extract facts and quotes."
    args_schema: type[BaseModel] = ScrapeArgs

    def _run(self, url: str, max_chars: int = 4000) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; CrewAIResearchBot/1.0)"}
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            html = resp.text
        except Exception as e:
            logger.exception("ScrapeUrlTool request failed")
            return f"Scrape failed for {url}: {e}"

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        parts = []
        for el in soup.find_all(["h1", "h2", "h3", "p", "li"]):
            txt = el.get_text(" ", strip=True)
            if txt:
                parts.append(txt)
        text = "\n".join(parts).strip()
        return text[:max_chars] if text else "No readable text found."
