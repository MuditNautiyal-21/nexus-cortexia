# Nexus Cortexia: Quickstart

Pick your platform. Follow the three lines underneath. Go.

---

## Claude Code (terminal / VS Code extension)

```
cp -r nexus-cortexia/ ~/.claude/skills/
cp nexus-cortexia/commands/* ~/.claude/commands/
```

Then in any project:

```
/nexus Build me a markdown-to-PDF converter with watch mode
```

The first time you invoke it, Claude will read the protocol files. After that
they're cached. You can also just ask naturally ("build me a REST API for X")
and Claude Code will auto-trigger the skill based on the description.

**Windows (PowerShell):**
```powershell
Copy-Item -Recurse nexus-cortexia "$env:USERPROFILE\.claude\skills\"
Copy-Item nexus-cortexia\commands\* "$env:USERPROFILE\.claude\commands\"
```

---

## Claude Desktop

1. Open any project in Claude Desktop.
2. Go to **Project instructions** (the settings gear on the project).
3. Paste the full contents of `nexus-cortexia/SKILL.md` into the instructions.
4. Save.

To invoke, either:
- Say "use nexus" or "run the full pipeline" in your message, or
- Prefix with a bracket: `[NEXUS] Build me a Slackbot that summarizes PRs.`

If your project involves more than a trivial script, it'll auto-trigger from
phrases like "build me", "create a system", "implement", or "architect."

---

## Cursor

1. Create `.cursorrules` in your project root (or edit the existing one).
2. Paste the contents of `nexus-cortexia/SKILL.md` into it.
3. Also copy the `skills/`, `agents/`, `references/`, and `profiles/`
   subfolders into the project root, or keep them nested under
   `nexus-cortexia/` and adjust the paths in SKILL.md accordingly.

Invoke with bracketed triggers: `[NEXUS] Refactor auth to use JWT with refresh tokens.`

Cursor's agent mode will follow the protocol. The slash commands won't work
(Cursor doesn't have Claude Code-style commands) but the bracket invocation
does.

---

## Windsurf

Same as Cursor, but the rules file is `.windsurfrules` instead of `.cursorrules`.

---

## VS Code (with GitHub Copilot or Continue)

1. Create `.github/copilot-instructions.md` (Copilot) or `.continue/config.json`
   (Continue) in your workspace.
2. For Copilot: paste the SKILL.md content into `copilot-instructions.md`.
3. For Continue: add SKILL.md content as a custom system message.

Invoke with `[NEXUS] <your project>`.

---

## ChatGPT, Gemini, or any other LLM

Paste the full contents of `nexus-cortexia/SKILL.md` at the top of a new
conversation (or into the system prompt if your tool supports it). That's it.

To run the pipeline, prefix your request with a bracket trigger:

```
[NEXUS] Build me a CLI that monitors a directory and posts changed files to a webhook.
```

The LLM will read the protocol, decompose the project, debate the approach,
execute, and review. Quality depends on the model — works well on GPT-4 and
above, Gemini Pro and above, and Claude at any capability level. Weaker
models may struggle with the decomposition stage.

---

## Local models (Ollama, LM Studio, llama.cpp)

Works with any local model that supports a system prompt and has decent
instruction-following (Llama 3 70B+, Mistral Large, DeepSeek V2+, Qwen 72B+).

1. Load SKILL.md as the system prompt.
2. Prefix requests with `[NEXUS]`.

Smaller models (7B-13B) generally can't handle multi-stage orchestration.
Expect the protocol to degrade on them, especially the consensus phase.

---

## Verifying it works

After installing, paste this exact message:

```
[NEXUS] Build me a Python script that reads a CSV, filters rows where age > 18, and writes the result to a new CSV.
```

You should see:

1. A task graph with 3-5 atomic tasks, grouped into 1-2 waves.
2. A pause asking for your approval.
3. After approval: implementation with inline comments, a self-review, and a
   token usage report.

If you get plain code with no decomposition, the skill didn't load. Check the
installation step for your platform.

---

## Profiles at a glance

| Profile | Token cost | When to use |
|---------|-----------|-------------|
| `lean` | 40-60% of standard | Tight budget, simple projects |
| `standard` (default) | baseline | Most work |
| `thorough` | 150-200% of standard | Production, security-critical, high-stakes |

Invoke a profile with `/nexus:lean`, `/nexus:thorough`, or the bracket
equivalent `[NEXUS:LEAN]`, `[NEXUS:THOROUGH]`.
