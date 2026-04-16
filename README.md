# Nexus Cortexia

An orchestration brain you drop into any AI coding environment. It makes the
AI decompose projects before building, debate approaches before committing,
and stop wasting tokens on context it doesn't need. No API keys, no installs,
no configuration.

## What it actually does

Most AI coding assistants jump straight to code. They write something, you
point out what's wrong, they rewrite it, and the cycle repeats until either
the code works or you've spent 300K tokens getting there.

Nexus Cortexia breaks that cycle with five mandatory protocols:

1. **Decompose** the project into the smallest possible tasks before touching code
2. **Debate** approaches from multiple angles before committing (adaptive: skips when unnecessary)
3. **Execute** with clean, task-scoped context (no history accumulation)
4. **Review** every non-trivial piece of code before calling it done
5. **Guard tokens** throughout, compressing context, routing cheap tasks to cheap models

The result: fewer rewrites, fewer wasted tokens, and code that works on
the first or second attempt instead of the fifth.

## Install in 30 seconds

### Claude Code

```bash
git clone https://github.com/YOUR_USERNAME/nexus-cortexia.git
cp -r nexus-cortexia ~/.claude/skills/
cp nexus-cortexia/commands/* ~/.claude/commands/
```

You now have these slash commands:

- `/nexus <project>` — full pipeline
- `/nexus:decompose <project>` — planning only
- `/nexus:debate <question>` — consensus on a single decision
- `/nexus:execute` — run the approved task graph
- `/nexus:review <file>` — two-stage code review
- `/nexus:resume` — continue a saved session
- `/nexus:lean <project>` — lean profile
- `/nexus:thorough <project>` — thorough profile

Or skip the commands entirely and just ask Claude to "build me X" — the
skill auto-triggers on common patterns.

### Claude Desktop

Paste `SKILL.md` into your project's instructions (gear icon → Project
instructions). Invoke with `[NEXUS] <your request>` or natural phrases like
"build me a..." or "use nexus cortexia on this."

### Cursor / Windsurf

Copy `SKILL.md` contents into `.cursorrules` (Cursor) or `.windsurfrules`
(Windsurf). Also copy the `skills/`, `agents/`, `references/`, and
`profiles/` folders into your project root. Invoke with bracket triggers:
`[NEXUS] <your request>`.

### Any other AI (ChatGPT, Gemini, local models)

Paste `SKILL.md` as a system prompt or into the first message. Invoke with
bracket triggers: `[NEXUS] <your request>`.

### Upload as a file

Most chat interfaces let you upload files. Upload `SKILL.md` and tell the
AI to follow it. Invoke with `[NEXUS] <your request>`.

**For full per-platform instructions with verification steps, see [QUICKSTART.md](./QUICKSTART.md).**

## How to invoke (three options)

| Method | Works on | Example |
|--------|----------|---------|
| Slash commands | Claude Code | `/nexus Build me a PR summary bot` |
| Bracket trigger | Everything | `[NEXUS] Build me a PR summary bot` |
| Natural language | Everything | `Build me a PR summary bot, use the full pipeline` |

All three produce the same result. Pick what fits your muscle memory.

## Project structure

```
nexus-cortexia/
├── SKILL.md                 # Main entry point. Start here.
├── QUICKSTART.md            # Per-platform setup and verification
├── commands/                # Slash commands for Claude Code
│   ├── nexus.md             # /nexus
│   ├── nexus-decompose.md   # /nexus:decompose
│   ├── nexus-debate.md      # /nexus:debate
│   ├── nexus-execute.md     # /nexus:execute
│   ├── nexus-review.md      # /nexus:review
│   ├── nexus-resume.md      # /nexus:resume
│   ├── nexus-lean.md        # /nexus:lean
│   └── nexus-thorough.md    # /nexus:thorough
├── skills/
│   ├── core/SKILL.md        # Behavioral rules (always active)
│   ├── decomposer/SKILL.md  # Task decomposition protocol
│   ├── consensus/SKILL.md   # Multi-perspective debate protocol
│   ├── executor/SKILL.md    # Implementation dispatch
│   ├── reviewer/SKILL.md    # Two-stage code review
│   └── token-guard/SKILL.md # Token optimization (always active)
├── agents/
│   ├── architect.md         # Designs approaches
│   ├── implementer.md       # Writes code
│   ├── reviewer.md          # Finds bugs
│   └── tester.md            # Writes tests
├── references/
│   ├── protocol-spec.md     # Full protocol spec (AI-system agnostic)
│   └── token-strategies.md  # Token optimization playbook
├── profiles/
│   ├── lean.md              # Budget mode: minimum tokens
│   ├── standard.md          # Default: balanced
│   └── thorough.md          # Quality mode: production-grade rigor
├── hooks/
│   └── session-persistence.md # Save/restore state across sessions
└── examples/
    ├── simple-project.md    # Walkthrough: CLI tool (~7K tokens)
    └── complex-project.md   # Walkthrough: full-stack app (~77K tokens)
```

## How it's different from just asking Claude to "plan first"

Telling an AI "plan before you code" works sometimes. The problem is
inconsistency. Sometimes it plans. Sometimes it skips straight to code.
Sometimes the plan is vague hand-waving that doesn't prevent any mistakes.

Nexus Cortexia makes the discipline mandatory and specific:

- Decomposition has a defined output format (task DAG with dependency edges)
- Consensus has a defined protocol (propose, review, vote, escalate threshold)
- Execution has defined context rules (stateless agents, compressed dependencies)
- Review has defined severity levels and block/pass criteria

It's the difference between "try to eat healthy" and a specific meal plan.

## Token savings

A comparison based on real project patterns:

| Project type | Without Nexus Cortexia | With Nexus Cortexia | Savings |
|-------------|----------------------|---------------------|---------|
| Small CLI tool | 15K-25K tokens | 7K-15K tokens | 40-55% |
| Medium web app | 80K-150K tokens | 40K-80K tokens | 45-55% |
| Large multi-service | 200K-400K tokens | 80K-160K tokens | 50-65% |

The savings come from fewer retries (because the plan was solid), less
context waste (because agents are stateless), and compressed handoffs
(because dependency outputs are summarized to interfaces).

## Works with

- Claude Code and Claude Desktop (primary target)
- Cursor, Windsurf, and VS Code with AI extensions
- OpenAI ChatGPT and GPT-based coding tools
- Google Gemini
- Any LLM that can follow multi-step instructions from a system prompt

## Profiles

Pick the mode that fits your situation:

**Lean**: minimum tokens. Skip most discussion, brief reviews. For budget
runs or simple projects. (~40-60% of standard cost)

**Standard** (default): debate for moderate tasks, full review for non-trivial
work. The sweet spot for most projects.

**Thorough**: full debate for everything, TDD, security review pass. For
production-critical code. (~150-200% of standard cost)

Tell the AI which profile to use: "Use nexus-cortexia in lean mode" or
"thorough mode for this one."

## Contributing

The whole thing is markdown files. Fork the repo, edit the files, send
a PR. No build step, no dependencies, no package managers.

If you're adding a new skill or agent role, follow the existing patterns:
one file per concept, clear when-to-use guidance, specific-not-vague
instructions.

## License

MIT. Use it, modify it, sell it, ship it. Attribution appreciated but
not required.
