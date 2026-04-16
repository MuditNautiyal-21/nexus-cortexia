# Session persistence

How to save and restore Nexus Cortexia state across sessions. Useful when a
project spans multiple conversations.

## What to save

At the end of a session, save to `.nexus-cortexia/state.json`:

```json
{
  "project_aim": "Build a task management API",
  "task_graph": { ... },
  "completed_tasks": ["task-1", "task-2", "task-3"],
  "current_wave": 2,
  "agreed_approaches": {
    "task-4": "Use JWT with 15-minute expiry...",
    "task-5": "Redis-backed session store..."
  },
  "compressed_outputs": {
    "task-1": "User model: id, email, password_hash...",
    "task-2": "Database: PostgreSQL, migrations via Alembic..."
  }
}
```

## What to restore

At the start of the next session, read the state file and pick up where you
left off. You have the task graph, you know what's done, and you have
compressed outputs from completed work. No need to re-plan or re-discuss
finished tasks.

## When to persist

- End of any session where the project isn't finished
- After completing each wave (natural checkpoint)
- Before any risky operation (in case it fails and you need to roll back)

## Cleanup

Delete `.nexus-cortexia/` when the project is complete. It's working state,
not part of the deliverable.

## Claude Code hook integration

If using Claude Code hooks, you can automate this with a post-session hook
that writes the state file. The Nexus Cortexia skill will check for it
automatically at the start of each session.
