---
name: nexus-cortexia-token-guard
description: Token optimization protocol. Runs throughout every phase.
---

# Token Guard protocol

This isn't a phase you run once. It's a set of constraints that apply to
every single response, every agent dispatch, every context injection, from
start to finish.

The problem with most multi-agent setups is they hemorrhage tokens. Agent A
generates 2000 tokens, passes all of it to Agent B, who generates 2000 more
and passes everything to Agent C. By Agent D, you're carrying 8000 tokens of
context that's 80% irrelevant. Token Guard prevents this.

## The rules

### 1. No accumulated history

Each agent call starts fresh. No conversation history from previous tasks.
The only context an agent receives is:
- Its role prompt (fixed, ~200 tokens)
- The current task spec (~200-400 tokens)
- The agreed approach (~300-500 tokens)
- Compressed dependency outputs (~200-500 tokens)

Total input per task: 900-1600 tokens. Compare this to the 10,000-30,000
tokens you'd spend if you carried the full conversation history.

### 2. Compress dependency outputs

When task B depends on task A's output, don't pass A's full implementation.
Pass only what B needs to know:

**Instead of** (2000 tokens):
```python
# Full user_model.py implementation
class User(BaseModel):
    id: int
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Config:
        orm_mode = True

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
# ... 80 more lines
```

**Pass this** (150 tokens):
```
User model (user_model.py):
  Fields: id (int), email (str, validated), password_hash (str),
          created_at (datetime), is_active (bool)
  Methods: verify_password(password: str) -> bool
  Uses: Pydantic BaseModel, bcrypt for password verification
  ORM mode enabled.
```

### 3. Structured output for decisions

When making choices, returning votes, or producing task specs, use JSON.
It's denser than prose and parseable by downstream consumers.

Prose decision (120 tokens):
> After careful consideration, I believe we should use PostgreSQL for the
> database because our data model has several many-to-many relationships
> that benefit from proper foreign key constraints, and the query patterns
> we'll need are well-suited to a relational database.

Structured decision (40 tokens):
```json
{"decision": "postgresql", "reason": "many-to-many FKs, complex queries"}
```

### 4. Terse responses

Every response should answer the question with minimal words. If someone asks
"what's the status?" the answer is "3 of 5 tasks done, currently on task 4"
not a three-paragraph update.

Rules of thumb:
- If it can be said in one sentence, use one sentence
- If it needs a list, use a list. Don't pad each item into a paragraph
- Code speaks for itself. Don't explain obvious code

### 5. Smart model routing

When subagents are available and the hosting platform supports model
selection:

| Task type | Recommended model | Why |
|-----------|------------------|-----|
| Decomposition | Fast/cheap (Haiku, 4o-mini) | Planning, not coding |
| Discussion synthesis | Fast/cheap | Summarization task |
| Context compression | Fast/cheap | Mechanical, not creative |
| Implementation | Full model (Sonnet, 4o) | Needs code quality |
| Review | Full model | Needs critical thinking |
| Final integration | Full model | Needs precision |

This cuts 30-50% off total token cost because planning and summarization
tasks don't need the expensive model.

### 6. Skip work that doesn't earn its tokens

- Skip consensus for trivial tasks (saves ~3000 tokens per skip)
- Skip review for trivial tasks (saves ~1000 tokens per skip)
- Don't decompose projects that are already small enough to implement in
  one pass (saves ~1500 tokens)
- Don't re-read files you read earlier in the same task

### 7. Iterative retrieval over bulk loading

Don't load an entire codebase into context "just in case." Read only the
files you need, when you need them. If you realize mid-task that you need
another file, read it then. Three targeted reads of 100 lines each costs
less than one bulk read of 3000 lines.

### 8. Lazy-load phase-specific sub-SKILLs

The main `SKILL.md` lists paths like `skills/decomposer/SKILL.md`,
`skills/consensus/SKILL.md`, `skills/executor/SKILL.md`, etc. Don't read
all of them upfront.

Read them only when the phase actually starts:

- Entering decomposition? Read `skills/decomposer/SKILL.md` now.
- Starting a consensus round? Read `skills/consensus/SKILL.md` now.
- About to dispatch tasks? Read `skills/executor/SKILL.md` now.
- About to review? Read `skills/reviewer/SKILL.md` now.

Skip the read entirely for phases the project won't use. A trivial task
that skips consensus doesn't need the consensus protocol in context. A
project that skips decomposition (because it's already one small task)
doesn't need the decomposer protocol loaded at all.

Once a phase finishes, the sub-SKILL can drop out of active context. The
main `SKILL.md` summary is enough to navigate to the next phase.

## Token budget tracking

After each major phase, report approximate token usage:

```
Decomposition:                     ~1,200 tokens
Consensus (4 tasks, 1 escalated):  ~14,000 tokens
Execution (8 tasks):               ~32,000 tokens
Review (6 reviews):                ~8,000 tokens
Total:                             ~55,200 tokens
```

This helps the user understand where their tokens went and whether the
overhead of planning and discussion paid off in the form of fewer retries
and rewrites.

## Profile modes

For different situations, different token discipline levels:

**Lean mode** (read: `profiles/lean.md`): maximum compression. Skip all
optional discussion. Terse output only. For budget-conscious runs or
simple projects.

**Standard mode** (default): the balance described above. Discussion for
non-trivial tasks, compression between phases, normal output verbosity.

**Thorough mode** (read: `profiles/thorough.md`): full discussion for every
task, detailed reviews, deeper test coverage. Higher token spend, higher
quality. For production-critical or security-sensitive work.
