# Changelog

All notable changes to Nexus Cortexia will be recorded here. This project
follows [Semantic Versioning](https://semver.org/).

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
