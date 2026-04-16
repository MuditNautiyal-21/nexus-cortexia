---
description: Execute an already-decomposed task graph. Use after /nexus:decompose has been approved.
argument-hint: [optional: specific task ID or "all"]
---

Load the Nexus Cortexia executor protocol: `nexus-cortexia/skills/executor/SKILL.md`.

Execute the approved task graph from the current session. Follow the wave
structure. Dispatch independent tasks to subagents in parallel when available,
sequentially otherwise.

For each non-trivial task, run the consensus protocol before coding. Review
every non-trivial output before marking it done.

If I passed a specific task ID, execute only that task plus any unfinished
prerequisites. If I passed "all" or nothing, execute the entire remaining graph.

Argument: $ARGUMENTS
