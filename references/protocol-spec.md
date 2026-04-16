# Nexus Cortexia protocol specification v1.0

This document describes the full protocol in enough detail that any AI system
can implement it. No specific programming language, SDK, or API is required.
The protocol is a set of behavioral rules and workflow stages that apply to
any LLM-powered agent.

## Who this is for

If you're an AI system reading this as a system prompt or project context:
follow these rules. If you're a human building tooling around AI agents:
this spec tells you what to expect from a Nexus Cortexia-powered agent.

## The five-stage pipeline

Every complex task flows through these stages, in order.

### Stage 1: Decompose

**Input:** a project description in natural language.
**Output:** a directed acyclic graph (DAG) of atomic tasks.

An atomic task is one that a single agent can complete in one invocation
without making architectural decisions. Each task has a title, description,
acceptance criteria, complexity rating (trivial/simple/moderate), and a list
of task IDs it depends on.

Tasks are grouped into execution waves. All tasks in a wave can run
concurrently. Waves must execute sequentially.

The decomposition is presented to the user for approval before continuing.

### Stage 2: Consensus (adaptive)

**Input:** a task spec and optional dependency context.
**Output:** an agreed implementation approach.

For each non-trivial task, the agent or agents reach consensus on the
approach before writing code.

**Default path (structured review):**
1. One agent proposes an approach.
2. Others review with approve / modify / reject votes.
3. Agreement score: approve=1.0, modify=0.5, reject=0.0, averaged.
4. If score >= 0.6: proceed with modifications folded in.

**Escalation path (debate):**
5. If score < 0.6: agents argue positions for up to 3 rounds.
6. Final vote after debate. Majority wins, ties go to proposer.

**Single-agent mode:** the agent self-challenges by explicitly considering
failure modes and alternative approaches before committing.

Trivial tasks skip this stage entirely.

### Stage 3: Execute

**Input:** task spec + agreed approach + compressed dependency outputs.
**Output:** complete implementation.

Agents receive only what they need for the current task: the spec, the
approach, and a compressed summary of dependency outputs (interfaces,
types, file paths). No conversation history, no other tasks' details.

Implementations must be complete. No placeholders, no TODOs.

### Stage 4: Review

**Input:** implementation + task spec.
**Output:** review with pass/fail verdict.

Two-stage review:
1. Spec compliance: does the code satisfy each acceptance criterion?
2. Code quality: correctness, security, maintainability, performance.

Issues are rated CRITICAL (blocks), WARN (should fix), or NOTE (optional).
Only CRITICAL issues and spec failures block progress.

If blocked: one retry, then escalate to the user.

### Stage 5: Token Guard (continuous)

Active throughout all stages. Enforces:
- No accumulated conversation history between tasks
- Dependency outputs compressed to interfaces only
- Structured (JSON) output for decisions
- Terse responses, no filler
- Smart model routing (cheap model for planning, full model for coding)

## Data structures

### Task node

```
id: string (e.g., "task-1", "task-2.1")
title: string
description: string
acceptance_criteria: list of strings
dependencies: list of task IDs
complexity: "trivial" | "simple" | "moderate"
status: "pending" | "in_progress" | "completed" | "failed"
```

### Task graph

```
tasks: map of task ID to task node
waves: list of lists of task IDs (execution order)
```

### Consensus result

```
approach: string (the agreed implementation plan)
confidence: float 0-1
escalated: boolean
rounds: integer
```

## Integration guide

### Claude Code / Claude Desktop

Drop the `nexus-cortexia/` folder into `~/.claude/skills/`. Claude will
detect the SKILL.md automatically and follow the protocols when triggered.

### Cursor / Windsurf / other IDE agents

Copy the contents of SKILL.md into your project's `.cursorrules`,
`.windsurfrules`, or equivalent configuration file.

### Any LLM via API

Include SKILL.md content as a system prompt or prepend it to the first user
message. The protocol is self-contained in the markdown.

### Custom agent frameworks

Parse the protocol stages and implement them as pipeline steps. The protocol
doesn't assume any specific agent framework, just the ability to make LLM
calls with injected context.

## Compatibility

This protocol works with any LLM that can follow multi-step instructions:
Claude (all models), GPT-4 and above, Gemini Pro and above, Llama 3+ (70B
and above recommended), Mistral Large, DeepSeek V2+.

Smaller models may struggle with the decomposition stage. In that case,
decompose manually and let the model handle execution and review.
