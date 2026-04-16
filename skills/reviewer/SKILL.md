---
name: nexus-cortexia-reviewer
description: Two-stage code review protocol. Catches bugs before they compound.
---

# Reviewer protocol

Every non-trivial implementation gets reviewed before it counts as done.
The review has two stages (borrowed from the Superpowers pattern, because
it works): first check if it does what the spec says, then check if the
code itself is good.

Separating these stages keeps the reviewer focused. Mixing "does it meet
the spec?" with "is this variable named well?" produces muddled reviews
that miss the important issues.

## Stage 1: Spec compliance

Check whether the implementation actually satisfies the task specification.

For each acceptance criterion:
- Does the code handle it? (yes / no / partially)
- If partially or no: what's missing?

This is a pass/fail check. Either the criterion is met or it isn't. No
gray area, no "well, it sort of works if you squint."

If any criterion fails, stop here. The code needs a fix before it's worth
reviewing for quality.

## Stage 2: Code quality

Once spec compliance passes, review the code itself:

**Correctness.** Does the logic actually do what it claims? Walk through the
main paths mentally. Check the edge cases the developer might have missed.
Off-by-one errors, null handling, empty inputs, concurrent access.

**Security.** Any injection vectors? Unsanitized inputs? Hardcoded secrets?
Overly broad permissions? This matters even for internal tools. Especially
for internal tools, actually, since those tend to get less scrutiny.

**Maintainability.** Will someone understand this code in 6 months without
the original context? Are the names descriptive? Is the flow followable?
Are there comments where the logic is non-obvious?

**Performance.** Any obvious bottlenecks? N+1 queries, unnecessary loops over
large datasets, missing indexes? Don't micro-optimize, but do flag the things
that will cause actual problems.

## Review output format

Keep reviews specific and actionable. No vague "could be improved" without
saying how.

```
## Spec compliance
- [PASS] Criterion 1: handles valid input correctly
- [FAIL] Criterion 2: returns 200 instead of 201 on creation
- [PASS] Criterion 3: rate limiting works

## Code quality
- [CRITICAL] Line 45: SQL query uses string interpolation. Use parameterized
  queries to prevent injection.
- [WARN] Line 72: catching bare Exception swallows errors you probably want
  to see. Catch specific exceptions.
- [NOTE] Line 90-95: this loop could be a list comprehension, but the current
  form is fine for readability.

## Verdict: NEEDS FIX (1 spec failure, 1 critical issue)
```

## Severity levels

**CRITICAL**: must fix before the code ships. Security vulnerabilities,
incorrect behavior, data loss risks.

**WARN**: should fix. Code smells, potential bugs, maintainability concerns.
These can wait if there's a time crunch, but they'll bite you later.

**NOTE**: optional improvements. Style suggestions, minor refactors,
performance micro-optimizations. Take them or leave them.

A review blocks progress only if there are CRITICAL issues or spec failures.
WARN and NOTE issues should be addressed if practical, but don't hold up the
pipeline.

## Retry policy

If the review finds CRITICAL issues:

1. Send the specific issues back to the implementer
2. The implementer gets one retry to fix them
3. After the retry, review the fix only (don't re-review the whole thing)
4. If the retry still fails, flag it for the user. Two failed attempts means
   the task spec or approach might need rethinking.

## Self-review (single-agent mode)

When you're both implementer and reviewer, switch mental modes before
reviewing. Put down the "I wrote this and it's great" hat and pick up the
"what's wrong with this?" hat.

Specifically ask yourself:
- "What input would break this?"
- "What happens if the network call fails?"
- "What happens with empty data?"
- "Did I actually test this, or am I assuming it works?"
- "Would I approve this code from someone else?"

Self-review is harder than reviewing someone else's code because you have to
fight confirmation bias. Force yourself to look for problems.
