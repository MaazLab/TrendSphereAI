from __future__ import annotations

import logging
from typing import Optional
from pydantic import BaseModel, Field

from crewai.tools import BaseTool

logger = logging.getLogger(__name__)

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except Exception:
    PYTRENDS_AVAILABLE = False


class TrendArgs(BaseModel):
    topic: str = Field(..., description="Topic keyword to query")
    geo: Optional[str] = Field(None, description="Two letter country code like US or DE")
    timeframe: str = Field("today 12-m", description="Google Trends timeframe")


class GoogleTrendsTool(BaseTool):
    name: str = "trend_insights"
    description: str = (
        "Fetch top and rising related queries for a topic using Google Trends. "
        "Outputs two lists with values."
    )
    args_schema: type[BaseModel] = TrendArgs

    def _run(self, topic: str, geo: Optional[str] = None, timeframe: str = "today 12-m") -> str:
        if not PYTRENDS_AVAILABLE:
            return "Trends not available. Install pytrends to enable this tool."

        try:
            pytrends = TrendReq(hl="en-US", tz=360)
            pytrends.build_payload([topic], cat=0, timeframe=timeframe, geo=geo or "", gprop="")
            related = pytrends.related_queries() or {}
            item = related.get(topic, {}) or {}
            rising = item.get("rising")
            top = item.get("top")

            def to_lines(df, header):
                if df is None or df.empty:
                    return []
                rows = df.sort_values("value", ascending=False).head(10).to_dict(orient="records")
                lines = [header]
                lines += [f"- {r.get('query')} ({r.get('value')})" for r in rows if r.get("query")]
                return lines

            lines = []
            lines += to_lines(top, "Top related queries:")
            lines += to_lines(rising, "\nRising related queries:")
            return "\n".join(lines) if lines else "No trend data available for this topic."
        except Exception as e:
            logger.exception("GoogleTrendsTool failed")
            return f"Trend insights failed: {e}"
