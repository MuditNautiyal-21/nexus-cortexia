# Example: building a CSV-to-JSON CLI tool

This walkthrough shows Nexus Cortexia handling a small project end to end.

## User prompt

> Build a Python CLI tool that converts CSV files to JSON with support for
> custom column mapping.

## Phase 1: Decompose

```
Task graph: csv-to-json converter

Simple CLI with one core function and some configuration options.

Wave 1 (2 tasks, parallel)
- [task-1] Set up project structure and CLI argument parsing (trivial)
  Create main.py with argparse: input file, output file, mapping file (optional).
  Acceptance: runs with --help and shows usage.

- [task-2] Write CSV parsing and column mapping logic (simple)
  Read CSV with csv module. If mapping file provided (JSON dict of old->new
  column names), apply it. Return list of dicts.
  Acceptance: correctly maps {"name": "full_name"} on a test CSV.

Wave 2 (1 task, after wave 1)
- [task-3] Write JSON output and wire everything together (simple)
  Connect the CLI args to the CSV parser, write JSON output.
  Handle errors: file not found, invalid CSV, bad mapping file.
  Acceptance: end-to-end conversion works. Error messages are clear.

Wave 3 (1 task, after wave 2)
- [task-4] Write tests (simple)
  Test happy path, empty CSV, missing file, invalid mapping.
  Acceptance: all tests pass.

Summary: 4 tasks in 3 waves. 1 trivial, 3 simple. No consensus needed.
```

User: "Looks good, go ahead."

## Phase 2: Consensus

Skipped. All tasks are trivial or simple, and the approach is unambiguous.

## Phase 3: Execute

Tasks 1 and 2 implemented in parallel. Task 3 implemented after. Task 4
after that. Total: 4 complete files, all working.

## Phase 4: Review

Quick self-review catches one issue: task-3 didn't handle the case where
the output directory doesn't exist. Fixed in-place, no retry needed.

## Phase 5: Token summary

```
Decomposition:    ~800 tokens
Execution:        ~6,200 tokens
Review:           ~400 tokens
Total:            ~7,400 tokens
```

Compare to an unstructured conversation doing the same work: typically
15,000-25,000 tokens because of back-and-forth clarification and iterative
refinement. The planning overhead paid for itself.
