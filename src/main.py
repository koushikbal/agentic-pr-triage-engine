import argparse
from src.config import get_settings
from src.github_client import GitHubClient
from src.state import TriageState
def main():
    parser = argparse.ArgumentParser(description="Agentic PR Triage & Auto-Fix Engine"); parser.add_argument("--repo", required=True); parser.add_argument("--pr", type=int, required=True); parser.add_argument("--run-id", type=int, required=True); args = parser.parse_args()
    settings = get_settings(); github = GitHubClient(settings.github_token)
    state = TriageState(repo_name=args.repo, pr_number=args.pr, run_id=args.run_id, raw_logs=github.fetch_workflow_logs(args.repo, args.run_id))
    raise RuntimeError(f"State collected for {state.repo_name}; configure an OpenAI Responses client before running the graph")
if __name__ == "__main__": main()

