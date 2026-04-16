---
description: Resume a Nexus Cortexia project from a saved state file. Picks up where the last session left off.
---

Load `nexus-cortexia/hooks/session-persistence.md` for the state format.

Look for `.nexus-cortexia/state.json` in the current project. If it exists:

1. Read the saved task graph, completed task list, agreed approaches, and
   compressed outputs.
2. Report what was already done and what's still pending.
3. Ask whether I want to continue with the next pending wave or change the
   plan first.

If no state file exists, tell me and suggest running `/nexus` to start fresh.

Do not start executing automatically. Show me the status first.
