# backend/app/tools/keywords.py
import re
import math
from typing import List, Optional, Dict, Any
from collections import Counter, defaultdict
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

_STOPWORDS = {
    "a","an","the","and","or","but","of","to","for","in","on","by","with","is","are",
    "was","were","be","been","being","that","this","it","as","at","from","into","over",
    "than","then","so","such","via","about","your","you","we","our","they","their","i",
    "me","my","mine","us","them","he","she","his","her","hers","its","not","no","yes",
    "do","does","did","done","can","could","should","would","may","might","will","just"
}

def _clean(text: str) -> str:
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\w\s-]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()

def _tokens(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", text) if t not in _STOPWORDS]

def _ngrams(tokens: List[str], n: int) -> List[str]:
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def _score_phrases(text: str, topic: Optional[str], max_keywords: int) -> List[Dict[str, Any]]:
    cleaned = _clean(text)
    toks = _tokens(cleaned)

    # base frequencies
    uni = Counter(toks)
    bi = Counter(_ngrams(toks, 2))
    tri = Counter(_ngrams(toks, 3))

    # merge to a dict: phrase -> score
    scores = defaultdict(float)
    for term, f in uni.items():
        scores[term] += f * 1.0
    for term, f in bi.items():
        # favor 2-grams (readable keyphrases)
        scores[term] += f * 2.0
    for term, f in tri.items():
        # 3-grams a bit lower than bigrams to avoid verbosity
        scores[term] += f * 1.5

    # topic boost
    if topic:
        topic_l = topic.lower()
        for term in list(scores.keys()):
            if any(tok in term for tok in _tokens(topic_l)):
                scores[term] *= 1.3

    # length prior (mildly favor 2-3 word phrases)
    for term in list(scores.keys()):
        nwords = len(term.split())
        scores[term] *= (1.0 + 0.1 * min(nwords, 3))

    # prune noisy short tokens
    items = [
        {"term": t, "score": round(s, 4)}
        for t, s in scores.items()
        if not t.isdigit() and len(t) >= 2
    ]

    # sort by score desc, keep top N, dedupe by lowercase
    items.sort(key=lambda x: x["score"], reverse=True)
    seen = set()
    deduped = []
    for it in items:
        key = it["term"].lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(it)
        if len(deduped) >= max_keywords:
            break
    return deduped

class KeywordArgs(BaseModel):
    text: str = Field(..., description="Input text from which to extract keywords/phrases")
    topic: Optional[str] = Field(None, description="Topic hint to bias ranking")
    max_keywords: int = Field(25, ge=5, le=50, description="Max keywords to return")

class KeywordSuggestTool(BaseTool):
    name: str = "keyword_suggest_tool"
    description = (
        "Tool Name: keyword_suggest_tool\n"
        "Tool Arguments: {'text': 'Input text', 'topic': 'Optional topic hint', 'max_keywords': 'int 5-50'}\n"
        "Tool Description: Extracts & ranks 1-3 word keywords/phrases without external APIs."
    )
    args_schema = KeywordArgs

    def _run(self, text: str, topic: Optional[str] = None, max_keywords: int = 25) -> Dict[str, Any]:
        kw = _score_phrases(text, topic, max_keywords)
        return {"topic": topic, "count": len(kw), "keywords": kw}

def keyword_suggest_tool():
    return KeywordSuggestTool()
