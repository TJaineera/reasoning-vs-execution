from typing import Dict, Any, Tuple

PROTECTED_FILES = {
    ".env",
    ".gitignore",
    "requirements.txt",
    "README.md",
}

DESTRUCTIVE_ACTIONS = {"DELETE_FILE", "WRITE_FILE", "OVERWRITE_FILE"}


def validate_plan(plan: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Decide whether the system will allow execution.
    This is intentionally dumb and strict.
    """
    confidence = plan.get("confidence", "LOW")
    tool_result = plan.get("tool_result", {})
    tool_status = tool_result.get("status", "UNKNOWN")

    # If our tool itself says "NO_MATCHES", we treat that as uncertainty.
    if tool_status == "NO_MATCHES":
        # Not automatically blocked — but we downgrade trust.
        pass

    for action in plan.get("actions", []):
        action_type = action.get("type")
        path = action.get("path", "")

        # Block destructive actions on protected files
        if path in PROTECTED_FILES and action_type in DESTRUCTIVE_ACTIONS:
            return False, f"Blocked: protected file '{path}'"

        # Block destructive actions if confidence is low
        if action_type in DESTRUCTIVE_ACTIONS and confidence == "LOW":
            return False, "Blocked: low-confidence destructive action"

    return True, "OK"

