from unittest.mock import Mock
from src.graph import build_graph
from src.state import TriageState
def test_graph_retries_failed_verification(tmp_path):
    github = Mock(); llm = Mock(); github.get_pull_request_files.return_value = {"app.py": "raise ValueError()\n"}
    llm.responses.create.side_effect = [Mock(output_text='{"patch":"diff --git a/app.py b/app.py\\n--- a/app.py\\n+++ b/app.py\\n@@ -1 +1 @@\\n-raise ValueError()\\n+pass\\n"}')] * 3
    result = build_graph(github, llm, workspace=str(tmp_path)).invoke(TriageState(repo_name="o/r", pr_number=1, run_id=2, raw_logs="ValueError: bad"))
    assert result["verification_attempts"] == 3
