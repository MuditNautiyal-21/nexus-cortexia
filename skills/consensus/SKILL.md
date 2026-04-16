---
name: nexus-cortexia-consensus
description: Multi-perspective consensus protocol. Agents debate approaches before committing to code.
---

# Consensus protocol

The idea is simple: before writing code for anything non-trivial, think about
it from multiple angles. Catch the bad ideas before they become bad code. In a
multi-agent setup, different agents argue the positions. In single-agent mode,
you simulate the perspectives yourself.

This sounds expensive. It isn't, because it uses an adaptive approach: start
cheap, escalate only when there's genuine disagreement.

## The adaptive flow

```
PROPOSE ──> REVIEW ──> [agreement?]
                          │
                  yes: synthesize and proceed
                  no:  escalate to DEBATE ──> VOTE ──> synthesize
```

### Phase 1: Propose

One perspective (the architect's viewpoint) generates a concrete approach.
Not vague hand-waving. Specific:

- Which patterns and abstractions to use
- What the file structure looks like
- What the key interfaces are
- Where the tricky parts are and how to handle them
- What could go wrong

This takes one agent turn. Cheap.

### Phase 2: Review

Other perspectives review the proposal. Each reviewer votes:

- **Approve**: looks good, build it
- **Modify**: right direction, but change X and Y
- **Reject**: wrong approach, here's why

Each review is brief: a vote, a rationale (2-3 sentences), and specific
suggested changes if applicable. This takes one turn per reviewer. Still cheap.

### Agreement check

Calculate a score: approve = 1.0, modify = 0.5, reject = 0.0. Average
across reviewers.

- **Score >= 0.6**: consensus reached. Fold in the "modify" suggestions,
  synthesize a final plan, move on.
- **Score < 0.6**: genuine disagreement. Escalate.

The 0.6 threshold is a tunable default, not a measured optimum. Lower it
(to 0.5 or 0.4) if you want fewer escalations and are willing to accept
more "modify" suggestions as good-enough consensus. Raise it (to 0.75)
if you want tighter agreement before proceeding. The user can override
for the session with "use a consensus threshold of X" and the executor
should respect that for subsequent decisions.

Most tasks resolve here. The proposal is usually decent, the reviewers catch
a few things, the modifications get folded in, everyone moves on. This is
the 80% case, and it costs only 2-3 agent turns total.

### Phase 3: Debate (only when needed)

When reviewers reject, there's a real disagreement that needs resolution.
Each perspective argues their position in 1-2 focused paragraphs, directly
addressing the concerns raised by others. No rehashing agreed points.

Maximum 3 rounds. If you can't resolve it in 3 rounds, the disagreement is
probably about taste rather than correctness. Don't keep spinning.

### Phase 4: Vote

After debate, everyone votes one final time. Majority wins.

**On a tie, escalate to the user.** Present the competing approaches side
by side with the key trade-offs and ask which to pick. Don't default to
the original proposer. That bias toward the first instinct is exactly what
consensus is supposed to prevent, and a tie after three rounds of debate
is a signal the decision matters enough for the human to make it.

### Phase 5: Synthesize

Take the winning approach, fold in any agreed modifications from the process,
and write a clean, actionable implementation plan. This is what the executor
receives.

## In single-agent mode

You don't have other agents, so you simulate the perspectives:

1. **Propose** an approach.
2. **Challenge yourself**: "What are three ways this could go wrong? Is there a
   simpler alternative? What would a security-focused reviewer flag? What would
   a performance-focused reviewer flag?"
3. **Decide**: incorporate the valid concerns, discard the ones that don't apply.

This takes one extra think-step before implementation. It's not as rigorous
as a real multi-agent debate, but it catches the obvious mistakes, and that's
most of the value.

## When to skip consensus

Skip it when:

- The task is trivial (boilerplate, config files, simple CRUD)
- The approach is obvious and unambiguous
- The user already specified exactly how they want it done
- You're fixing a bug with a clear root cause

Run it when:

- The task involves architectural decisions
- There are multiple reasonable approaches
- The task touches security, auth, or data integrity
- You're uncertain about the right approach
- The task has "moderate" complexity

## Token cost of consensus

In the happy path (no escalation):
- 1 proposal turn
- 1-2 review turns
- 1 synthesis turn (using cheap model)
- Total: 3-4 turns, roughly 2000-4000 tokens

With escalation:
- Add 3-6 debate turns + 1 vote turn
- Total: 8-11 turns, roughly 6000-10000 tokens

Escalation happens maybe 20% of the time. The other 80% resolves in review.
Average cost across all tasks: roughly 3000 tokens per consensus round. For
context, a single badly-planned implementation attempt that has to be thrown
away and redone costs 8000-16000 tokens. The math works out.

## Discussion compression

Between rounds, compress the discussion to its essential points. Drop the
pleasantries, the "I agree with agent-2 that..." preambles, and the repeated
context. Keep: the decision, the key concern, the specific suggestion.

This prevents the discussion transcript from ballooning across rounds.

Before:
> Agent-1: I think we should use PostgreSQL because it has better support for
> complex queries and our data model has several many-to-many relationships
> that would benefit from proper foreign key constraints...
> [150 more words of rationale]

After compression:
> Agent-1: PostgreSQL. Reason: many-to-many relationships need FK constraints.
