#!/usr/bin/env python3
"""
validate_state.py

Validates .nexus-cortexia/state.json against the schema documented in
hooks/session-persistence.md. Run this before /nexus:resume if you've
edited state.json by hand or received it from someone else.

Usage:
    python3 scripts/validate_state.py [path/to/state.json]

If no path is given, defaults to ./.nexus-cortexia/state.json
Exits 0 on valid, 1 on any validation failure. Prints specific failures.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SUPPORTED_SCHEMA_VERSION = "1.0.0"
VALID_COMPLEXITIES = {"trivial", "simple", "moderate", "hard"}
VALID_PROFILES = {"lean", "standard", "thorough"}

# Phrases that look like prompt injection if found in free-text fields.
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous",
    r"disregard\s+(all\s+)?previous",
    r"forget\s+(everything|all|your\s+rules)",
    r"system\s*:\s*",
    r"</?\s*(system|assistant|user)\s*>",
    r"new\s+instructions?\s*:",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")


def warn(msg: str) -> None:
    print(f"WARN: {msg}")


def scan_for_injection(text: str, field: str) -> list[str]:
    hits = []
    for pat in INJECTION_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            hits.append(f"'{field}' contains suspicious phrase matching /{pat}/")
    return hits


def validate(state: dict) -> list[str]:
    errors: list[str] = []

    # Required top-level fields
    required = ["version", "project_aim", "task_graph", "completed_tasks"]
    for key in required:
        if key not in state:
            errors.append(f"missing required field: {key}")

    if errors:
        return errors

    # Version
    version = state.get("version", "")
    if version != SUPPORTED_SCHEMA_VERSION:
        warn(f"state.json version '{version}' differs from supported '{SUPPORTED_SCHEMA_VERSION}'")

    # project_aim
    aim = state.get("project_aim", "")
    if not isinstance(aim, str) or not (1 <= len(aim) <= 500):
        errors.append("project_aim must be a string between 1 and 500 chars")
    else:
        injection_hits = scan_for_injection(aim, "project_aim")
        errors.extend(injection_hits)

    # task_graph
    tg = state.get("task_graph")
    if not isinstance(tg, dict) or "tasks" not in tg:
        errors.append("task_graph must be an object with a 'tasks' array")
        return errors
    tasks = tg.get("tasks")
    if not isinstance(tasks, list) or len(tasks) == 0:
        errors.append("task_graph.tasks must be a non-empty array")
        return errors

    # Per-task validation
    task_ids: set[str] = set()
    for i, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(f"tasks[{i}] must be an object")
            continue
        for field in ("id", "title", "complexity", "depends_on", "wave"):
            if field not in task:
                errors.append(f"tasks[{i}] missing '{field}'")
        tid = task.get("id")
        if tid in task_ids:
            errors.append(f"duplicate task id: {tid}")
        if isinstance(tid, str):
            task_ids.add(tid)
        cx = task.get("complexity")
        if cx not in VALID_COMPLEXITIES:
            errors.append(f"tasks[{i}] complexity '{cx}' not in {VALID_COMPLEXITIES}")
        wave = task.get("wave")
        if not isinstance(wave, int) or wave < 1:
            errors.append(f"tasks[{i}] wave must be a positive integer")
        deps = task.get("depends_on", [])
        if not isinstance(deps, list):
            errors.append(f"tasks[{i}] depends_on must be a list")
        # Injection scan on title + description
        for field in ("title", "description"):
            val = task.get(field)
            if isinstance(val, str):
                errors.extend(scan_for_injection(val, f"tasks[{i}].{field}"))

    # Dependency references
    for i, task in enumerate(tasks):
        deps = task.get("depends_on", [])
        if isinstance(deps, list):
            for dep in deps:
                if dep not in task_ids:
                    errors.append(f"tasks[{i}] depends_on unknown task: {dep}")

    # Cycle detection via DFS
    graph = {t.get("id"): t.get("depends_on", []) for t in tasks if isinstance(t, dict)}

    def has_cycle(node, visiting, visited):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dep in graph.get(node, []):
            if has_cycle(dep, visiting, visited):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    for tid in list(graph.keys()):
        if has_cycle(tid, set(), set()):
            errors.append(f"cycle detected in dependency graph at task: {tid}")
            break

    # completed_tasks refs
    completed = state.get("completed_tasks", [])
    if not isinstance(completed, list):
        errors.append("completed_tasks must be an array")
    else:
        for tid in completed:
            if tid not in task_ids:
                errors.append(f"completed_tasks references unknown task: {tid}")

    # Optional fields
    profile = state.get("profile")
    if profile is not None and profile not in VALID_PROFILES:
        errors.append(f"profile '{profile}' not in {VALID_PROFILES}")

    failed = state.get("failed_tasks", [])
    if failed and not isinstance(failed, list):
        errors.append("failed_tasks must be an array of {task_id, reason, retry_count} objects")

    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".nexus-cortexia/state.json")
    if not path.exists():
        fail(f"file not found: {path}")
        return 1
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"invalid JSON: {e}")
        return 1
    except OSError as e:
        fail(f"cannot read file: {e}")
        return 1

    errors = validate(state)
    if errors:
        print(f"Validation FAILED for {path}:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"OK: {path} is valid against schema v{SUPPORTED_SCHEMA_VERSION}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
