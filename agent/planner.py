from pathlib import Path
from typing import Dict, Any


def propose_plan(repo_path: Path, tool_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Minimal 'planner' that mimics a model's behavior:
    - sees tool output
    - makes an inference
    - proposes actions + assumptions + confidence
    """
    target = tool_result.get("target_file", ".env")
    status = tool_result.get("status")
    confidence = tool_result.get("confidence", "LOW")

    actions = []
    assumptions = []

    if status == "NO_MATCHES":
        # This is the "allowed to guess" moment.
        assumptions.append("No references implies the file is unused.")
        assumptions.append("Unused files are safe to delete.")
        actions.append({
            "type": "DELETE_FILE",
            "path": target,
            "reason": "No references found in codebase"
        })
    else:
        assumptions.append("References exist, so deletion is risky.")
        actions.append({
            "type": "NOOP",
            "path": target,
            "reason": "References detected"
        })
        confidence = "HIGH"

    plan = {
        "repo": str(repo_path),
        "actions": actions,
        "assumptions": assumptions,
        "confidence": confidence,
        "tool_result": tool_result,
    }
    return plan

