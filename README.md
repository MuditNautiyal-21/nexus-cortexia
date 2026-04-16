# Nexus Cortexia

A drop-in orchestration protocol for AI coding workflows. Does planning,
decomposition, multi-agent dispatch, state persistence, and prompt-injection
defense. It also costs more tokens than a bare agent on the same work. Worth
knowing before you install.

## What it does

Coding assistants like to jump straight into code. They write, you point out
what broke, they rewrite. Nexus Cortexia tries to break that loop by
front-loading the thinking:

1. Decompose the project into the smallest tasks that make sense, with
   explicit dependencies.
2. Debate approaches before committing, or skip the debate when the answer
   is obvious.
3. Execute with task-scoped context so each sub-agent sees only what it
   needs.
4. Review non-trivial code before calling it done.
5. Watch the token budget, compress context between waves, lazy-load
   sub-skills.

Whether that pays off depends on the task. The numbers are below.

## Install in 30 seconds

### Claude Code

```bash
git clone https://github.com/YOUR_USERNAME/nexus-cortexia.git
cp -r nexus-cortexia ~/.claude/skills/
cp -r nexus-cortexia/commands/* ~/.claude/commands/
```

Slash commands:

- `/nexus <project>` runs the full pipeline
- `/nexus:decompose <project>` planning only
- `/nexus:debate <question>` one decision, multi-angle review
- `/nexus:execute` runs an approved task graph
- `/nexus:review <file>` two-stage code review
- `/nexus:resume` picks up a saved session
- `/nexus:lean`, `/nexus:thorough` switch profiles

### Claude Desktop

Paste `SKILL-compact.md` (about 3KB) into Project instructions. The full
`SKILL.md` is too large for Desktop's budget. Invoke with
`[NEXUS] your request`.

### Cursor, Windsurf, VS Code AI

Copy `SKILL.md` into `.cursorrules` or `.windsurfrules`, plus the `skills/`,
`agents/`, `references/`, and `profiles/` folders. Invoke with `[NEXUS]`.

### Other LLMs (ChatGPT, Gemini, local)

Paste `SKILL.md` or `SKILL-compact.md` as a system prompt. Invoke with
`[NEXUS]`. Weaker models tend to drift out of protocol partway through;
check the output.

Per-platform setup with verification steps: [QUICKSTART.md](./QUICKSTART.md).

## Performance

I benchmarked three conditions on two tasks. These are the numbers I got,
not the numbers I wanted.

### Small task: CSV filter CLI (about 150 LOC)

| Condition | Tokens | Tool calls | Wall-clock | Tests |
|---|---|---|---|---|
| Bare agent | 39,039 | 17 | 68.6s | 30 |
| Skill, single-agent | 38,282 | 9 | 62.5s | 19 |

About 2% token savings, 47% fewer tool calls, 6 seconds faster. Fine.

### Medium task: SQLite task tracker (about 1500 LOC)

| Condition | Tokens | Tool calls | Wall-clock | Tests | Integration bugs |
|---|---|---|---|---|---|
| Bare agent | 48,336 | 26 | 124s | 65 | 0 |
| Skill, single-agent | 57,590 | 31 | 154s | 66 | 0 |
| Skill, multi-agent (8 subagents, 6 waves) | 359,781 | 167 | ~712s | 130 | 1 |

Single-agent skill mode spent 19% more tokens and took 24% longer than a
bare agent. Multi-agent mode spent 7.4x the tokens of a bare agent, took
5.7x longer, and shipped with an integration bug: two subagents wrote
reasonable code in isolation, and the seam between them deadlocked on a
nested SQLite connection. The orchestrator had to patch it.

### What to take from this

The skill does not save tokens on small or medium work. Breaks even on
small, loses on medium. If cost is the thing you care about, run a bare
agent.

Reasons to use it anyway:

- The protocol produces slightly cleaner code. Fewer deprecated APIs, more
  defensive edge-case handling, less variation between modules.
- A programmatic state validator lets you resume mid-project after a crash
  or a context reset without re-planning.
- The decomposition and consensus stages leave an audit trail, which
  matters for work that needs one.
- Multi-agent dispatch is the only way forward when the project is too big
  to fit in one agent's context window. The token cost comes with the
  scale.

If none of those apply, the bare agent wins.

Benchmark tasks and raw subagent outputs are reproducible via scripts in
`benchmarks/` (currently tracked in the issue tracker; will be added to the
repo in a follow-up).

## How it differs from asking Claude to "plan first"

Telling an AI to plan before coding works sometimes. The rest of the time
it plans vaguely, or not at all, or plans a thing that prevents no bugs.
The skill makes the discipline specific:

- Decomposition has a defined output (task DAG with dependency edges,
  cycle-checked before execution).
- Consensus has a defined protocol: propose, review, vote, escalate on low
  agreement.
- Execution has context rules: stateless subagents, compressed dependency
  summaries.
- Review has severity levels and explicit pass/block criteria.

"Try to eat healthy" versus a specific meal plan.

## Project structure

```
nexus-cortexia/
├── SKILL.md                 # Main entry
├── SKILL-compact.md         # 3KB version for small instruction budgets
├── QUICKSTART.md
├── SECURITY.md              # Threat model, prompt-injection defenses
├── CHANGELOG.md
├── commands/                # Claude Code slash commands
│   ├── nexus.md
│   └── nexus/
│       ├── decompose.md, debate.md, execute.md
│       ├── review.md, resume.md
│       └── lean.md, thorough.md
├── skills/
│   ├── core/        # Always-active rules
│   ├── decomposer/
│   ├── consensus/
│   ├── executor/
│   ├── reviewer/
│   └── token-guard/
├── agents/          # Role prompts for multi-agent dispatch
├── scripts/
│   ├── validate_state.py    # State validator with DAG cycle + injection scan
│   ├── test_validator.py
│   └── check_ai_tells.py
├── references/
├── profiles/        # lean, standard, thorough
├── hooks/           # session-persistence
└── examples/
```

## Single-agent vs multi-agent

Both modes run the same protocols.

Single-agent runs them sequentially inside one LLM. This is the default on
Claude Desktop, ChatGPT, Gemini, and Cursor chat. Most platforms support
nothing else.

Multi-agent dispatches parallel subagents per wave via the Task tool. Only
Claude Code supports it cleanly today. The benchmark showed it did not save
wall-clock time in practice: one slow subagent gates the entire wave, and
integration bugs between subagents sometimes need orchestrator
intervention. Its real use case is projects that do not fit in a single
agent's context, where the cost is the price of scale.

## Profiles

Three modes, tell the AI which one:

- Lean: minimum tokens, brief reviews, skips most debate. About 40-60% of
  standard cost.
- Standard (default): debate on moderate decisions, full review on
  non-trivial code.
- Thorough: debate everything, TDD, security pass. About 150-200% of
  standard.

Usage: "use nexus-cortexia in lean mode" or "thorough mode for this one."

## Works with

Primary: Claude Code, Claude Desktop. Tested and tuned here.

Best-effort: Cursor, Windsurf, VS Code AI extensions, ChatGPT, Gemini, and
other LLMs that follow multi-step system prompts. Slash commands are
Claude Code only; elsewhere, use bracket triggers.

## Contributing

All markdown. Fork, edit, PR. No build step, no dependencies.

If you run your own benchmark, open an issue or PR with the numbers. n=2 is
small. More data would improve the Performance claims in either direction.

## License

MIT.
