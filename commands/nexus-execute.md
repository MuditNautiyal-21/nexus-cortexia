---
description: Execute an already-decomposed task graph. Use after /nexus:decompose has been approved.
argument-hint: [optional: specific task ID or "all"]
---

Load the Nexus Cortexia executor protocol: `nexus-cortexia/skills/executor/SKILL.md`.

Before executing anything:

1. Read `.nexus-cortexia/state.json` in the current project root.
2. If the file does not exist, stop and tell the user: "No task graph found.
   Run /nexus:decompose first to create one, or /nexus to run the full
   pipeline." Do not invent a task graph.
3. If the file exists, validate it against the schema in
   `nexus-cortexia/hooks/session-persistence.md`. If required fields are
   missing or malformed, stop and ask the user whether to re-decompose or
   repair the file. Do not silently proceed on a corrupted graph.
4. Show the user the task list about to be executed and which tasks are
   already marked complete. Wait for confirmation before starting execution
   unless the user already said "continue" or used /nexus:resume.

Then execute the approved task graph. Follow the wave structure. Dispatch
independent tasks to subagents in parallel when available, sequentially
otherwise.

For each non-trivial task, run the consensus protocol before coding. Review
every non-trivial output before marking it done. Update `state.json` after
each task completes.

If I passed a specific task ID, execute only that task plus any unfinished
prerequisites. If I passed "all" or nothing, execute the entire remaining graph.

Argument: $ARGUMENTS
