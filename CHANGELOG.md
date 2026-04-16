# Changelog

All notable changes to Nexus Cortexia will be recorded here. This project
follows [Semantic Versioning](https://semver.org/).

## [1.0.1] - 2026-04-16

Follow-up review pass. Addresses real bugs and gaps found in the initial
release.

### Fixed
- Slash command files moved from `commands/nexus-*.md` (flat) to
  `commands/nexus/*.md` (nested) so the documented `/nexus:decompose`
  colon syntax actually works in Claude Code
- Install commands in `QUICKSTART.md` now use `cp -r` to recurse into the
  nested command subdirectory

### Added
- `scripts/validate_state.py`: programmatic validator for
  `.nexus-cortexia/state.json`, including DAG cycle detection and
  prompt-injection pattern scanning on free-text fields
- `scripts/test_validator.py`: self-test suite for the validator
- `scripts/check_ai_tells.py`: scanner for AI writing tells (em dashes,
  marketing vocabulary, negative parallelisms) with per-file exceptions
- `.github/workflows/lint.yml`: CI running link check, validator self-test,
  and AI-tell scanner on every push/PR
- `SKILL-compact.md`: compact variant for hosts with small instruction
  budgets (Claude Desktop, ChatGPT custom instructions)
- Dangerous-operations section in `skills/executor/SKILL.md`: explicit
  per-command user consent required for `rm -rf`, `sudo`, `curl | sh`,
  credential access, and outbound network calls
- Strengthened prompt-injection rules in `skills/core/SKILL.md`: explicit
  pattern list for flagging retrieved content
- Failure tracking in state.json schema: `failed_tasks` and `blocked_tasks`
  fields, plus documented retry/revert behavior
- Concurrency caveat in `hooks/session-persistence.md` (no locking; single
  session per project recommended)
- Consensus threshold tuning guidance in `skills/consensus/SKILL.md`
- Per-platform state persistence caveats in `QUICKSTART.md` (Claude
  Desktop, ChatGPT, Gemini have no persistent state between sessions)

## [1.0.0] - 2026-04-16

Initial public release.

### Added
- Core skill (`SKILL.md`) with the five-protocol pipeline: Decompose,
  Debate, Execute, Review, Token Guard
- Sub-skills under `skills/`: core behavioral rules, decomposer, consensus,
  executor, reviewer, token-guard
- Role prompts under `agents/`: architect, implementer, reviewer, tester
- Three profiles: lean, standard, thorough
- Session persistence format under `hooks/session-persistence.md` with JSON
  schema and validation rules
- Eight slash commands for Claude Code under `commands/`
- Three invocation methods: slash commands, bracket triggers, natural
  language
- Reference docs: `references/protocol-spec.md`,
  `references/token-strategies.md`
- Two walkthroughs: `examples/simple-project.md`,
  `examples/complex-project.md`
- `SECURITY.md` with prompt-injection threat model
- `QUICKSTART.md` with per-platform setup instructions

### Known limitations
- Token savings in `README.md` are design targets, not benchmarked numbers
- Non-Claude platforms are best-effort; the protocol is LLM-agnostic but
  slash commands and bracket triggers behave differently across hosts
- Weaker models may struggle with the decomposition stage
