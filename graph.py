from langgraph.graph import END, START, StateGraph
from src.state import TriageState
from src.nodes.log_parser import parse_logs
from src.nodes.context_builder import build_context
from src.nodes.patch_generator import generate_patch
from src.nodes.sandbox_verifier import verify_patch
from src.nodes.pr_creator import create_pr
def build_graph(github_client, llm_client, workspace=None):
    graph = StateGraph(TriageState)
    graph.add_node("parse_logs", parse_logs)
    graph.add_node("build_context", lambda s: build_context(s, github_client))
    graph.add_node("generate_patch", lambda s: generate_patch(s, llm_client))
    graph.add_node("verify_patch", lambda s: verify_patch(s, workspace=workspace))
    graph.add_node("create_pr", lambda s: create_pr(s, github_client))
    graph.add_edge(START, "parse_logs"); graph.add_edge("parse_logs", "build_context"); graph.add_edge("build_context", "generate_patch"); graph.add_edge("generate_patch", "verify_patch")
    graph.add_conditional_edges("verify_patch", lambda s: "generate_patch" if not s.sandbox_passed and s.verification_attempts < 3 else "create_pr")
    graph.add_edge("create_pr", END)
    return graph.compile()
