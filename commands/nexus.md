---
description: Run the full Nexus Cortexia pipeline on a project. Decompose, debate, execute, review.
argument-hint: [project description]
---

Activate Nexus Cortexia for this request.

Read `nexus-cortexia/SKILL.md` first to load the full protocol, then run every
stage end-to-end:

1. **Decompose** the project into atomic tasks with dependency waves. Present
   the plan and wait for my approval before building anything.
2. **Debate** the approach for each non-trivial task using the adaptive
   consensus protocol. Skip trivial tasks.
3. **Execute** the agreed plan. Dispatch to subagents in parallel where tasks
   are independent. Complete implementations only, no placeholders.
4. **Review** every non-trivial output. Fix CRITICAL issues before moving on.
5. **Token Guard** is active throughout. Report approximate token usage at
   the end.

Default profile: standard. If I say "lean" or "thorough" before or after the
project description, use that profile instead.

Project: $ARGUMENTS
