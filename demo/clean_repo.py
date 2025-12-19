from pathlib import Path
from agent.planner import propose_plan
from tools.file_search import find_references
from executor.rules import validate_plan
from executor.executor import execute_plan


def main():
    repo = Path("sample_repo").resolve()
    if not repo.exists():
        raise SystemExit("sample_repo/ not found. Did you create it?")

    # 1) Tool call: find references to `.env` (will return NO_MATCHES)
    tool_result = find_references(repo_path=repo, target_file=".env")

    # 2) Agent proposes plan based on tool outputs (this is where it "guesses")
    plan = propose_plan(repo_path=repo, tool_result=tool_result)

    # 3) System validates plan (boring guardrails)
    ok, reason = validate_plan(plan)

    # 4) Execute (dry-run by default)
    result = execute_plan(plan, allowed=ok, decision_reason=reason, dry_run=True)

    print("\n=== DEMO RESULT ===")
    print(f"Decision: {'ALLOWED' if ok else 'BLOCKED'}")
    print(f"Reason:   {reason}")
    print(f"Log:      {result['log_path']}")
    print("===================\n")


if __name__ == "__main__":
    main()

