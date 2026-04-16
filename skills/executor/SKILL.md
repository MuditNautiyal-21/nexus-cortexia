---
name: nexus-cortexia-executor
description: Implementation dispatch protocol. Turns agreed plans into working code.
---

# Executor protocol

You have a decomposed task graph and agreed approaches. Now build it. The
executor's job is to turn plans into working code without wasting tokens on
false starts or dead ends.

## Execution order

Follow the wave structure from the decomposition phase. Within each wave,
tasks are independent and can run in parallel.

```
Wave 1: all tasks in parallel → wait for completion
Wave 2: all tasks in parallel → wait for completion
...
Wave N: final tasks → done
```

If you have subagent access, dispatch wave tasks to separate agents. If you
don't, work through them one at a time within each wave.

## Task execution flow

For each task:

### 1. Load only what you need

Inject into the agent's context:
- The task spec (title, description, acceptance criteria)
- The agreed approach from the consensus phase
- Compressed outputs from dependency tasks (interfaces, schemas, file paths)

Do not include: the full decomposition, other tasks' specs, the debate
transcript, previous wave outputs that aren't dependencies.

### 2. Check existing code first

If the project already has code (editing an existing codebase rather than
building from scratch), read the relevant files before writing anything.
Understand the patterns already in use: naming conventions, file organization,
testing style. Match them.

### 3. Implement completely

Write the full implementation. Not a skeleton. Not a placeholder. Not "TODO:
implement this later." Working code that satisfies every acceptance criterion.

Include inline comments only for non-obvious logic. Don't comment `i += 1` but
do comment a regex that parses a specific format, or a business rule that would
confuse someone reading the code in six months.

### 4. Self-check before handing off

Before declaring the task done, verify:
- Does it compile/parse without errors?
- Does it handle the edge cases mentioned in the spec?
- Do the acceptance criteria actually pass?
- Are the interfaces compatible with what dependent tasks expect?

## Dispatching to subagents

When subagents are available, give each one a complete, self-contained brief:

```
You are an implementer agent. Build the following:

Task: [title]
Description: [what to build]
Acceptance criteria:
  - [criterion 1]
  - [criterion 2]

Agreed approach:
[The approach from the consensus phase]

Context from completed dependencies:
[Compressed outputs: interfaces, types, file paths]

Requirements:
- Write complete, working code
- Follow existing project conventions
- Handle edge cases from the spec
- No placeholders or TODOs
- Save outputs to: [path]
```

The subagent receives only this. No conversation history, no other tasks'
details, no debate transcripts. Clean context, focused execution.

## Handling failures

If a task fails (can't satisfy criteria, hits an unexpected blocker):

1. **Diagnose.** What specifically failed and why?
2. **Can you fix it in one retry?** If yes, fix it. If no, flag it.
3. **Report the failure clearly.** "Task X failed because Y. I attempted Z
   but it didn't resolve the issue. The user needs to decide how to proceed."

Don't silently produce broken code and hope nobody notices. Don't burn
tokens on retry loops. One attempt, one retry, then escalate.

## Parallel execution strategy

When dispatching subagents in parallel:

- **Independent tasks go together.** If tasks share no dependencies, they
  can run simultaneously.
- **Shared-state tasks run sequentially.** If two tasks modify the same file
  or data structure, run them in order to avoid merge conflicts.
- **Budget-aware batching.** If you have 8 tasks in a wave but only budget
  for 4 agents, split into two batches of 4.

## Integration after execution

After each wave completes:

1. Collect all outputs
2. Check for interface mismatches between task outputs (did one task expect
   a function signature that another task defined differently?)
3. Resolve any conflicts
4. Compress the wave's outputs for use by the next wave's dependency context

After all waves:

1. Check end-to-end consistency
2. Run any integration tests
3. Produce the final deliverable
4. Report completion with token usage breakdown

## Single-agent execution

Without subagents, work through tasks sequentially within each wave. Keep
a running compressed context of what you've built so far, just the
interfaces and paths, not the full code.

For each task:
1. Load the task spec and approach
2. Add compressed context from completed dependencies
3. Implement
4. Self-review (brief, catch obvious issues)
5. Compress the output for future reference
6. Move to the next task
