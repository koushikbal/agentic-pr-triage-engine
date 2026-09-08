from src.nodes.log_parser import parse_logs
from src.state import TriageState
def test_parse_python_traceback():
    state = TriageState(repo_name="o/r", pr_number=1, run_id=2, raw_logs="Traceback (most recent call last):\n  File 'app.py', line 8\nValueError: bad input")
    result = parse_logs(state)
    assert result["parsed_errors"]; assert result["parsed_errors"][0]["references"][0]["file"] == "app.py"

