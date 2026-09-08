import json
from src.state import TriageState
SYSTEM = "Return JSON with exactly one key, patch. patch must be a unified git diff. Make the smallest safe fix."
def generate_patch(state: TriageState, llm_client=None) -> dict:
    if llm_client is None: raise ValueError("An LLM client is required")
    prompt = json.dumps({"errors": state.parsed_errors, "context": state.code_context, "verification_feedback": state.status})
    response = llm_client.responses.create(model=getattr(llm_client, "model", "gpt-4o"), input=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}], temperature=0)
    data = json.loads(getattr(response, "output_text", "")); patch = data.get("patch", "")
    if not patch.startswith("diff --git"): raise ValueError("LLM returned a non-unified patch")
    return {"proposed_patch": patch, "status": "patch_generated"}
