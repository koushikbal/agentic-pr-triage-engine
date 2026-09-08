from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class TriageState(BaseModel):
    repo_name: str
    pr_number: int
    run_id: int
    raw_logs: str = ""
    parsed_errors: List[dict] = Field(default_factory=list)
    code_context: Dict[str, str] = Field(default_factory=dict)
    proposed_patch: Optional[str] = None
    verification_attempts: int = 0
    sandbox_passed: bool = False
    status: str = "initialized"

