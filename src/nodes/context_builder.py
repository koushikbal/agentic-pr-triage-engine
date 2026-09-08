from src.state import TriageState
def build_context(state: TriageState, github_client) -> dict:
    files = github_client.get_pull_request_files(state.repo_name, state.pr_number)
    refs = {ref["file"] for error in state.parsed_errors for ref in error.get("references", []) if ref.get("file")}
    return {"code_context": {p: c for p, c in files.items() if not refs or p in refs}, "status": "context_built"}

