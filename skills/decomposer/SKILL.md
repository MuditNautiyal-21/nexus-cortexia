---
name: nexus-cortexia-decomposer
description: Task decomposition protocol. Breaks projects into atomic implementable steps.
---

# Decomposer protocol

The goal: take a vague "build me X" and turn it into a concrete list of tasks
that could each be finished by a focused developer in one sitting. No task
should require the implementer to make architectural decisions. Those decisions
happen before implementation, in the debate phase.

## What "atomic" actually means

A task is atomic when all of these are true:

- One person (or one agent) can finish it in a single pass
- The inputs and outputs are clearly defined
- The acceptance criteria are specific and verifiable
- No architectural choices remain; it's just implementation
- Complexity is "trivial," "simple," or at most "moderate"

If a task would be "complex," it's not atomic yet. Break it down further.

## The decomposition process

### Step 1: Identify the top-level phases

Most software projects break into 3-7 natural phases. For a typical web app,
that might look like: data model, backend API, frontend UI, auth, tests,
deployment. For a CLI tool: argument parsing, core logic, output formatting,
error handling.

Don't force a structure. Let the project's shape suggest the phases.

### Step 2: Break each phase into concrete tasks

For each phase, ask: "What specific things need to be built?" Not vague things
like "implement the backend" but specific things like "create the POST /users
endpoint that validates email format and hashes the password."

Each task needs:

- **Title**: short, specific (not "implement feature" but "add JWT token refresh endpoint")
- **What to build**: 2-3 sentences describing the implementation
- **Acceptance criteria**: concrete checks. "Returns 401 for expired tokens" not
  "handles auth correctly"
- **Complexity**: trivial / simple / moderate
- **Dependencies**: which other tasks must finish first

### Step 3: Map the dependency graph

Draw the edges. Which tasks need outputs from which other tasks? A database
schema task probably blocks the API endpoint tasks. The API tasks probably
block the frontend tasks. Some tasks have no dependencies and can run in
parallel from the start.

### Step 4: Group into execution waves

Tasks with no unfinished dependencies can run at the same time. Group them
into waves:

```
Wave 1 (parallel): project setup, data model definition
Wave 2 (parallel, after wave 1): API endpoints, database migrations
Wave 3 (parallel, after wave 2): frontend components, integration tests
Wave 4: end-to-end tests, deployment config
```

### Step 5: Present and wait

Show the user the full task graph. Include:
- Total task count
- Number of parallel waves
- Estimated complexity distribution
- Any assumptions you made

Then stop and wait for approval. The user might want to add tasks, remove
tasks, change priorities, or correct your assumptions. Don't start building
until they sign off.

## Output format

```
# Task graph: [Project name]

[1-2 sentence summary of the approach]

## Wave 1 (N tasks, parallel)
- [task-1] Title — complexity
  Description. Acceptance: criteria.
- [task-2] Title — complexity
  Description. Acceptance: criteria.

## Wave 2 (N tasks, after wave 1)
- [task-3] Title [depends: task-1] — complexity
  Description. Acceptance: criteria.

## Summary
- Total: N implementable tasks in M waves
- Complexity: X trivial, Y simple, Z moderate
- Assumptions: [list any assumptions]

Approve this plan? I'll start building once you confirm.
```

## Common mistakes to avoid

**Too coarse.** "Build the API" is not a task, it's a category. Break it into
individual endpoints or logical groups.

**Too granular.** "Add import statement for json module" is not worth tracking.
Group related micro-steps into a single task.

**Missing dependencies.** If task B uses the output of task A, that dependency
must be explicit. Implicit dependencies cause failures when tasks run in
parallel.

**Assuming tech stack.** If the user hasn't specified a framework, language, or
database, ask before decomposing. The task structure depends on these choices.

## Recursive decomposition

If you're looking at a task marked "moderate" and it still feels like it needs
architectural decisions, decompose it further. You can go up to 4 levels deep
(task-1 → task-1.1 → task-1.1.1 → task-1.1.1.1). If you're hitting level 5,
the original project scope is probably too large for a single run.

## Adaptive sizing

Match decomposition depth to project size:

- **Small project** (1 file, <200 lines): 2-5 tasks, maybe 1-2 waves.
  Don't over-decompose a simple script.
- **Medium project** (3-10 files): 5-15 tasks, 2-4 waves.
- **Large project** (10+ files, multiple services): 15-30 tasks, 4-6 waves.
  Beyond 30 tasks, consider splitting into separate project runs.
