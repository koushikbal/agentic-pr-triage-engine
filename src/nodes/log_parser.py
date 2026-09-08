import re
from src.state import TriageState
TRACE_PATTERNS = [re.compile(r"Traceback \(most recent call last\):(?P<body>.*?)(?=\n\S.*(?:Error|Exception)|\Z)", re.S), re.compile(r"(?:Error|Exception):.*(?:\n.*){0,8}"), re.compile(r"(?:panic:|fatal error:).*", re.I)]
FILE_LINE = re.compile(r"(?P<file>[\w./\\-]+\.(?:py|js|ts|go))(?::(?P<line>\d+))?")
def parse_logs(state: TriageState) -> dict:
    text = state.raw_logs or ""
    matches = []
    for pattern in TRACE_PATTERNS: matches.extend(m.group(0).strip() for m in pattern.finditer(text))
    if not matches and text.strip(): matches = [line.strip() for line in text.splitlines() if re.search(r"\b(?:error|failed|exception|panic)\b", line, re.I)]
    errors = []
    for block in dict.fromkeys(matches):
        refs = [{"file": m.group("file"), "line": int(m.group("line")) if m.group("line") else None} for m in FILE_LINE.finditer(block)]
        errors.append({"message": block, "references": refs})
    return {"parsed_errors": errors, "status": "parsed"}

