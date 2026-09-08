import base64
import requests
from github import Github

class GitHubClient:
    def __init__(self, token: str, api_url: str = "https://api.github.com"):
        if not token:
            raise ValueError("GITHUB_TOKEN is required")
        self.api_url = api_url.rstrip("/")
        self.github = Github(token, base_url=api_url)
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})

    def fetch_workflow_logs(self, repo_name: str, run_id: int) -> str:
        response = self.session.get(f"{self.api_url}/repos/{repo_name}/actions/runs/{run_id}/logs", timeout=60)
        response.raise_for_status()
        return response.text

    def get_pull_request_files(self, repo_name: str, pr_number: int) -> dict[str, str]:
        repo = self.github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        result = {}
        for file in pr.get_files():
            content = repo.get_contents(file.filename, ref=pr.head.sha)
            if isinstance(content, list):
                continue
            result[file.filename] = base64.b64decode(content.content).decode("utf-8", errors="replace")
        return result

    def create_fix_pr(self, repo_name: str, base_branch: str, branch: str, files: dict[str, str], title: str, body: str) -> str:
        repo = self.github.get_repo(repo_name)
        base = repo.get_branch(base_branch)
        repo.create_git_ref(ref=f"refs/heads/{branch}", sha=base.commit.sha)
        for path, content in files.items():
            try:
                existing = repo.get_contents(path, ref=branch)
                repo.update_file(path, f"fix: update {path}", content, existing.sha, branch=branch)
            except Exception:
                repo.create_file(path, f"fix: add {path}", content, branch=branch)
        pr = repo.create_pull(title=title, body=body, head=branch, base=base_branch)
        return pr.html_url


