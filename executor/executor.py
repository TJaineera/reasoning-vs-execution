from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import json


def execute_plan(plan: Dict[str, Any], allowed: bool, decision_reason: str, dry_run: bool = True) -> Dict[str, Any]:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_path = logs_dir / f"run_{ts}.log"

    record = {
        "allowed": allowed,
        "decision_reason": decision_reason,
        "dry_run": dry_run,
        "plan": plan,
    }

    log_path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    # If blocked, do nothing
    if not allowed:
        return {"status": "BLOCKED", "log_path": str(log_path)}

    # If allowed but dry-run, do nothing
    if dry_run:
        return {"status": "DRY_RUN", "log_path": str(log_path)}

    # Optional: real execution (only if you later enable it)
    # For now, keep it safe.
    return {"status": "ALLOWED_BUT_NOT_EXECUTED", "log_path": str(log_path)}

