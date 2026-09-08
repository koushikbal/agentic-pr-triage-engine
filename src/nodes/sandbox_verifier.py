import subprocess, tempfile
from pathlib import Path
from src.state import TriageState
def verify_patch(state: TriageState, workspace: str | None = None, timeout: int = 300) -> dict:
    if not state.proposed_patch: return {"sandbox_passed": False, "verification_attempts": state.verification_attempts + 1, "status": "verification_failed: empty patch"}
    with tempfile.TemporaryDirectory() as temp:
        root = Path(workspace or temp)
        result = subprocess.run(["git", "apply", "--whitespace=nowarn", "-"], cwd=root, input=state.proposed_patch, text=True, capture_output=True, timeout=timeout)
        tests = subprocess.run(["python", "-m", "pytest", "-q"], cwd=root, text=True, capture_output=True, timeout=timeout) if result.returncode == 0 else result
        return {"sandbox_passed": tests.returncode == 0, "verification_attempts": state.verification_attempts + 1, "status": "verified" if tests.returncode == 0 else f"verification_failed: {tests.stdout}\n{tests.stderr}"}

