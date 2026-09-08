from src.state import TriageState
def create_pr(state: TriageState, github_client, base_branch: str = "main") -> dict:
    if not state.sandbox_passed: return {"status": "not_created"}
    branch = f"agentic/fix-run-{state.run_id}"
    url = github_client.create_fix_pr(state.repo_name, base_branch, branch, state.code_context, f"fix: resolve CI failure from run {state.run_id}", f"## Automated CI fix\n\n- Workflow run: `{state.run_id}`\n- PR: `#{state.pr_number}`\n- Verification attempts: `{state.verification_attempts}`\n")
    return {"status": f"pr_created:{url}"}
