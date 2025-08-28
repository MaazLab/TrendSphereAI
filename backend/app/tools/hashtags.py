# backend/app/tools/hashtags.py
import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

# Simple platform norms (feel free to tweak)
_PLATFORM_HASHTAG_COUNTS = {
    "linkedin": {"primary": 3, "niche": 4, "broad": 2, "max_total": 8},
    "x":        {"primary": 2, "niche": 2, "broad": 1, "max_total": 5},  # Twitter/X
    "twitter":  {"primary": 2, "niche": 2, "broad": 1, "max_total": 5},
    "instagram":{"primary": 5, "niche": 8, "broad": 5, "max_total": 25},
    "default":  {"primary": 3, "niche": 4, "broad": 2, "max_total": 8},
}

_BROAD_TAGS = [
    "AI","MachineLearning","Tech","Innovation","Data","Developer","DevCommunity",
    "Cybersecurity","Privacy","DataPrivacy","Compliance"
]

def _tagify(phrase: str, pascal: bool = True) -> Optional[str]:
    words = re.findall(r"[A-Za-z0-9]+", phrase)
    if not words:
        return None
    if pascal:
        tag = "".join(w.capitalize() for w in words)
    else:
        tag = "".join(words).lower()
    if not tag:
        return None
    if len(tag) > 30:
        tag = tag[:30]
    return f"#{tag}"

def _dedupe(seq: List[str]) -> List[str]:
    seen = set()
    out = []
    for s in seq:
        if s and s.lower() not in seen:
            seen.add(s.lower())
            out.append(s)
    return out

def _platform_counts(platform: str) -> Dict[str, int]:
    return _PLATFORM_HASHTAG_COUNTS.get(platform.lower(), _PLATFORM_HASHTAG_COUNTS["default"])

def _keywords_from_text(text: str) -> List[str]:
    # fallback: pick frequent tokens >3 chars
    toks = re.findall(r"[A-Za-z][A-Za-z0-9]{2,}", text)
    cnt = {}
    for t in toks:
        k = t.lower()
        cnt[k] = cnt.get(k, 0) + 1
    return [k for k, _ in sorted(cnt.items(), key=lambda x: x[1], reverse=True)[:20]]

class HashtagArgs(BaseModel):
    platform: str = Field("LinkedIn", description="Platform name")
    keywords: Optional[List[str]] = Field(None, description="Preferred keywords/phrases")
    text: Optional[str] = Field(None, description="Fallback text to derive keywords from")
    max_total: Optional[int] = Field(None, description="Override total hashtag cap")

class HashtagSuggestTool(BaseTool):
    name: str = "hashtag_suggest_tool"
    description: str = (
        "Tool Name: hashtag_suggest_tool\n"
        "Tool Arguments: {'platform': 'str', 'keywords': 'List[str]', 'text': 'str', 'max_total': 'int'}\n"
        "Tool Description: Builds Primary/Niche/Broad hashtags for a platform from keywords."
    )
    args_schema: type[BaseModel] = HashtagArgs

    def _run(self, platform: str = "LinkedIn",
             keywords: Optional[List[str]] = None,
             text: Optional[str] = None,
             max_total: Optional[int] = None) -> Dict[str, Any]:

        pascal = platform.lower() in {"linkedin","x","twitter"}
        kws = keywords or _keywords_from_text(text or "")
        kws = [k for k in kws if len(k) > 1]
        # Prioritize multiword phrases first, then single words
        multi = [k for k in kws if " " in k]
        single = [k for k in kws if " " not in k]
        ranked = multi + single

        # Build buckets
        counts = _platform_counts(platform)
        if max_total:
            counts["max_total"] = max_total

        primary = []
        niche = []
        # Primary from top-ranked
        for k in ranked:
            tag = _tagify(k, pascal=pascal)
            if tag:
                primary.append(tag)
            if len(primary) >= counts["primary"]:
                break

        # Niche from remainder (long-tail)
        for k in ranked[len(primary):]:
            tag = _tagify(k, pascal=pascal)
            if tag:
                niche.append(tag)
            if len(niche) >= counts["niche"]:
                break

        # Broad tags (static list filtered by topical matches if possible)
        broad = []
        text_blob = " ".join(kws).lower() + " " + (text or "").lower()
        for bt in _BROAD_TAGS:
            if len(broad) >= counts["broad"]:
                break
            # simple topical filter
            if any(key in text_blob for key in [bt.lower(), bt.lower().replace("community","developer")]):
                broad.append(f"#{bt}")

        # ensure at least one broad tag
        if not broad:
            broad = [f"#{_BROAD_TAGS[0]}"]

        # Combine & enforce total cap
        all_tags = _dedupe(primary + niche + broad)
        all_tags = all_tags[: counts["max_total"]]

        return {
            "platform": platform,
            "counts": counts,
            "primary": primary[:counts["primary"]],
            "niche": niche[:counts["niche"]],
            "broad": broad[:counts["broad"]],
            "all": all_tags,
            "note": f"{len(all_tags)} hashtags suggested"
        }

def hashtag_suggest_tool():
    return HashtagSuggestTool()
