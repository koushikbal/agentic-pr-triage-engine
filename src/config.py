from functools import lru_cache
from pydantic import BaseModel, Field
import os

class Settings(BaseModel):
    github_token: str = Field(default="", repr=False)
    openai_api_key: str = Field(default="", repr=False)
    llm_model: str = "gpt-4o"
    max_verification_attempts: int = 3
    sandbox_timeout_seconds: int = 300
    sandbox_image: str = "python:3.12-slim"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(github_token=os.getenv("GITHUB_TOKEN", ""), openai_api_key=os.getenv("OPENAI_API_KEY", ""), llm_model=os.getenv("LLM_MODEL", "gpt-4o"), max_verification_attempts=int(os.getenv("MAX_VERIFICATION_ATTEMPTS", "3")), sandbox_timeout_seconds=int(os.getenv("SANDBOX_TIMEOUT_SECONDS", "300")), sandbox_image=os.getenv("SANDBOX_IMAGE", "python:3.12-slim"))

@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()


