# Token optimization playbook

A reference for every trick Nexus Cortexia uses to keep token costs down
without sacrificing output quality. Some of these are built into the
protocols. Others are judgment calls you make case-by-case.

## Strategy 1: Stateless agents

The single biggest token saver. Instead of carrying conversation history
across tasks (which grows linearly with each exchange), each agent invocation
starts clean with only the context it needs.

**Cost without this:** a 10-task project with 2000 tokens per task accumulates
to 20,000 tokens of history by task 10, most of it irrelevant.

**Cost with this:** each task gets ~1500 tokens of context regardless of how
many tasks came before. Flat, predictable, cheap.

## Strategy 2: Context compression

When task B depends on task A's output, compress A's output before injecting
it into B's context. Keep interfaces, drop implementations.

**Compression checklist:**
- Function/method signatures: keep
- Class/type definitions: keep (abbreviated)
- File paths: keep
- Import statements: drop
- Full implementations: drop
- Comments: drop
- Test code: drop

A 2000-token implementation compresses to ~200 tokens of interface summary.
That's a 90% reduction per dependency handoff.

## Strategy 3: Skip optional work

Not every task needs every protocol stage. The protocol defines which stages
to skip based on complexity:

| Complexity | Decompose | Consensus | Execute | Review |
|-----------|-----------|-----------|---------|--------|
| Trivial   | -         | skip      | yes     | skip   |
| Simple    | -         | quick     | yes     | yes    |
| Moderate  | -         | full      | yes     | full   |

"Quick" consensus means the propose-review path without debate. It's 2-3
turns instead of 8-11.

Skipping consensus and review for a trivial task saves ~4000 tokens per task.
In a project with 5 trivial tasks, that's 20,000 tokens saved.

## Strategy 4: Structured output

JSON is denser than prose for the same information. Use it for:
- Task specs
- Votes and decisions
- Status updates
- Dependency summaries

Typical savings: 50-70% compared to prose equivalents.

## Strategy 5: Smart model routing

If your platform lets you choose models per-request:

**Cheap model (Haiku, 4o-mini, Gemini Flash):**
- Task decomposition
- Context compression and summarization
- Discussion synthesis
- Status formatting

**Full model (Sonnet, Opus, GPT-4o, Gemini Pro):**
- Code implementation
- Code review
- Architectural proposals
- Complex debugging

Planning tasks don't need the expensive model. They're organizational, not
creative. Routing them to Haiku/4o-mini cuts their cost by 70-90%.

## Strategy 6: Iterative retrieval

Don't pre-load everything. Read files when you need them, not before.

**Bad pattern:** read all 15 project files at the start "for context,"
consuming 30,000 tokens before you've done anything.

**Good pattern:** read the 2-3 files relevant to the current task when you
start that task. If you realize mid-task you need another file, read it then.

Three reads of 200 lines each: ~1800 tokens.
One bulk read of 3000 lines: ~9000 tokens.

## Strategy 7: Terse output conventions

Every word you generate costs tokens. These conventions trim the fat:

- No preambles ("Sure!", "Great question!")
- No postambles ("Let me know if you need more!")
- No restating the question
- No hedging when you're confident
- Lists over paragraphs when listing things
- Code over description when showing code

A typical Claude response contains 30-40% filler by token count. Cutting
that drops your output token costs by a third.

## Strategy 8: Batch similar work

If you have 5 small tasks that all modify the same file, batch them into
one edit session instead of five separate read-edit-write cycles. Each
cycle has overhead (reading the file, thinking about context, writing the
response). Batching pays that overhead once.

## Approximate token budgets by project size

These are rough guidelines. Actual costs vary with model, project complexity,
and how often consensus requires escalation.

| Project size | Tasks | Tokens (lean) | Tokens (standard) | Tokens (thorough) |
|-------------|-------|---------------|-------------------|-------------------|
| Small (1-2 files) | 3-5 | 8K-15K | 15K-25K | 25K-40K |
| Medium (5-10 files) | 8-15 | 25K-50K | 50K-80K | 80K-120K |
| Large (10+ files) | 15-30 | 50K-100K | 100K-160K | 160K-250K |

For comparison, a single unstructured Claude conversation building the same
project typically runs 150K-400K tokens because of accumulated context,
failed attempts, and back-and-forth clarification. Nexus Cortexia's overhead
(planning, consensus, review) usually pays for itself through fewer retries.
