# Nexus Cortexia

A drop-in orchestration layer for any AI coding environment. Makes the AI
plan before building, think through approaches before committing, and stop
wasting tokens on context it doesn't need. No API keys, no installs, no
configuration.

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

End result is less churn. Plans are solid before anything gets typed, so you
don't spend five rounds untangling bad code.

## Install in 30 seconds

### Claude Code

```bash
git clone https://github.com/YOUR_USERNAME/nexus-cortexia.git
cp -r nexus-cortexia ~/.claude/skills/
cp nexus-cortexia/commands/* ~/.claude/commands/
```

You now have these slash commands:

- `/nexus <project>` runs the full pipeline
- `/nexus:decompose <project>` for planning only
- `/nexus:debate <question>` for consensus on a single decision
- `/nexus:execute` runs the approved task graph
- `/nexus:review <file>` runs a two-stage code review
- `/nexus:resume` continues a saved session
- `/nexus:lean <project>` uses the lean profile
- `/nexus:thorough <project>` uses the thorough profile

Or skip the commands entirely and just ask Claude to "build me X". The skill
auto-triggers on common patterns.

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

## How to invoke

Each platform has a recommended primary method. The others work too, but
stick with the primary unless you have a reason.

| Platform | Primary | Also works |
|----------|---------|-----------|
| Claude Code | Slash commands: `/nexus Build me a PR summary bot` | Bracket trigger, natural language |
| Claude Desktop | Bracket trigger: `[NEXUS] Build me a PR summary bot` | Natural language |
| Cursor, Windsurf, VS Code AI | Bracket trigger | Natural language |
| ChatGPT, Gemini, other LLMs | Bracket trigger | Natural language |

Natural language ("build me a PR summary bot, use nexus cortexia") works
everywhere but is the least reliable. It depends on the model recognizing
the trigger phrase inside the skill description.

## Project structure

```
nexus-cortexia/
├── SKILL.md                 # Main entry point. Start here.
├── QUICKSTART.md            # Per-platform setup and verification
├── commands/                # Slash commands for Claude Code
│   ├── nexus.md             # /nexus
│   └── nexus/
│       ├── decompose.md     # /nexus:decompose
│       ├── debate.md        # /nexus:debate
│       ├── execute.md       # /nexus:execute
│       ├── review.md        # /nexus:review
│       ├── resume.md        # /nexus:resume
│       ├── lean.md          # /nexus:lean
│       └── thorough.md      # /nexus:thorough
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
│   └── thorough.md          # Quality mode: debate everything, TDD, security pass
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

These are **design targets**, not benchmarked numbers. Real savings depend on
the project, the model, and how strictly the skill gets followed. If you run
your own comparisons and want to contribute data, open a PR.

| Project type | Without Nexus Cortexia (estimate) | Target with Nexus Cortexia | Target savings |
|-------------|-----------------------------------|----------------------------|----------------|
| Small CLI tool | 15K-25K tokens | 7K-15K tokens | ~40-55% |
| Medium web app | 80K-150K tokens | 40K-80K tokens | ~45-55% |
| Large multi-service | 200K-400K tokens | 80K-160K tokens | ~50-65% |

The targets come from fewer retries (because the plan was solid), less
context waste (because agents are stateless), and compressed handoffs
(because dependency outputs are summarized to interfaces). Whether your
project hits those numbers depends on how well the model follows the
protocol and how much rework the original code needed.

## Works with

Primary target (tested and tuned for these):

- Claude Code
- Claude Desktop

Best-effort (the protocol is LLM-agnostic, but bracket triggers and
slash commands behave differently across platforms):

- Cursor, Windsurf, VS Code with AI extensions
- OpenAI ChatGPT and GPT-based coding tools
- Google Gemini
- Any other LLM that can follow multi-step instructions from a system prompt

On non-Claude platforms, expect to drop slash commands and rely on bracket
triggers or natural language. Quality varies with the model; weaker models
may struggle with the decomposition stage or drift out of protocol mid-run.

## Single-agent vs multi-agent

Nexus Cortexia works in both modes.

- **Single-agent mode** (the usual case on Claude Desktop, ChatGPT,
  Gemini, Cursor chat): one LLM runs all five protocols sequentially by
  itself. Decompose, then debate in its own head, then execute, then
  review. This is the default path on most platforms.
- **Multi-agent mode** (Claude Code with subagent dispatch, or any
  platform that supports task-level agent spawning): independent tasks in
  the same wave can run in parallel, and role prompts from `agents/` are
  injected into fresh agent contexts.

The protocols are the same either way. The only difference is whether the
waves run in parallel or sequentially. If your host supports subagents,
use them. If not, you still get the planning and review discipline.

## Profiles

Three modes, pick what fits:

- **Lean**: minimum tokens, skips most discussion, runs brief reviews. Good
  for tight budgets or simple projects. About 40-60% of standard cost.
- **Standard** (default): debate for moderate tasks, full review for
  non-trivial work. The usual pick.
- **Thorough**: full debate on everything, TDD, security review pass. For
  production code or anything where a bug costs real money. About 150-200%
  of standard.

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
