from __future__ import annotations
import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

try:
    from dotenv import find_dotenv, load_dotenv
except ImportError as e:
    raise RuntimeError(
        "Install python-dotenv to load .env automatically: pip install python-dotenv"
    ) from e

# 1) Find the .env starting from CWD and walking up to project root
ENV_FILE: str = find_dotenv(filename=".env", usecwd=True)

# 2) Load it into process env exactly once
if ENV_FILE:
    load_dotenv(dotenv_path=ENV_FILE, override=False)
else:
    # Optional: do not raise, but you can log here if you want
    pass

class Settings(BaseSettings):
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    tavily_api_key: str | None = Field(default=None, alias="TAVILY_API_KEY")
    llm_model: str = Field(default="gpt-4o-mini", alias="LLM_MODEL")

    # We rely on process env now, not an env_file path
    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()

# 3) Make sure libs that only read os.environ can see the keys
if settings.openai_api_key and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
if settings.tavily_api_key and not os.getenv("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = settings.tavily_api_key

# Optional: expose for debugging
ENV_PATH = Path(ENV_FILE) if ENV_FILE else None
