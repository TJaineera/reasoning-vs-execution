
from pathlib import Path
from typing import Dict, Any, List


def find_references(repo_path: Path, target_file: str) -> Dict[str, Any]:
    """
    Looks for occurrences of the target filename in .py files.
    Returns explicit uncertainty when none are found.
    """
    py_files = list(repo_path.rglob("*.py"))
    matches: List[str] = []

    for f in py_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if target_file in text:
            matches.append(str(f.relative_to(repo_path)))

    if not matches:
        return {
            "status": "NO_MATCHES",
            "confidence": "LOW",
            "target_file": target_file,
            "results": None,
            "note": "No references found. This might mean unused OR might mean the tool didn't capture runtime usage."
        }

    return {
        "status": "OK",
        "confidence": "MEDIUM",
        "target_file": target_file,
        "results": matches,
        "note": "References found in source files."
    }
