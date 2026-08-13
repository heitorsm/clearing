---
name: vault-diverge
description: |
  Grounded divergent ideation with qualified pruning, persisted to an Obsidian vault. Runs a 4-phase loop: Anchor (reframe + pruning contract + grounding brief from the vault), Diverge (N parallel isolated branches under cognitive frames via the divergent-generator agent), Qualified Pruning (convergent-critic agent scores against the contract, per-criterion verdicts, trap detection), Persist (synthesis note + top ideas enter the parking-lot incubation flow). Use on /diverge, "diverge", "divergir", "brainstorm", "ideate", "explore options for", "widen the search", "gerar ideias", "explorar opções", or open-ended design, architecture, naming, strategy, and fuzzy-problem decisions. Skip for syntax questions, lookups, problems with one canonical answer, or closed phrasing ("quick", "standard", "just"). Dual-mode: full experience with Obsidian CLI (vault-mode), degraded honest operation on project documents (artifact-mode). Expensive (~12 agent calls): the pre-flight gate in the skill body is mandatory unless explicitly invoked.
---

# Vault Diverge

Grounded divergence with qualified pruning. The first three answers any model gives are the answers a senior engineer gives in thirty seconds: correct, forgettable. The interesting answers live past number three. This skill walks there, but anchored in your vault, judged against a declared objective, and persisted so nothing is lost.

Adapted from the "adhd" divergent-ideation loop by UditAkhouri (MIT, github.com/UditAkhourii/adhd), with three structural additions: source grounding, a pruning contract, and vault persistence.

## Mode detection

Before anything, detect the operating mode once and announce it:

- Run `obsidian version`. If it responds and `obsidian vault` confirms an active vault: **vault-mode** (full experience).
- Otherwise: **artifact-mode**. Grounding reads the project documents available in context; persistence produces a versioned artifact (`current-divergence-<slug>.md`) for the user to store. State the degradation in one line, do not simulate vault features.

## Pre-flight gate

This skill costs ~12 agent calls, 5 to 10x a single answer. Run this gate before Phase 0.

**Step 1, explicit invocation.** If the user typed /diverge or explicitly asked for this skill, skip the rest of the gate and go to Phase 0.

**Step 2, self-judge.** Four checks; if any fails, ABORT and answer directly, optionally offering /diverge in one sentence.

1. Open-ended? Multiple viable answers exist. If canonical, abort.
2. High-stakes? The cost of the obvious answer being wrong is real (architecture, public API, naming a product, strategy, fuzzy bug with unknown root cause). If low, abort.
3. Open phrasing? The user avoided "quick", "standard", "canonical", "just", "one-line". If present, abort.
4. Validated problem or hypothesis? The problem is worth solving, or the user explicitly wants to explore an unvalidated hypothesis. If neither is clear, ask one question before proceeding; do not spend 12 calls on a problem nobody validated.

## Phase 0: Anchor

### 0.1 Reframe (before locking the objective)

The most expensive failure of divergence is mastering the wrong question. Before the contract, generate 2 to 3 reformulations of the stated objective and ask the user to pick (or keep the original):

- **Ladder up**: ask "why does this matter?" and reframe at the higher goal.
- **Ladder down**: ask "what specifically?" and reframe at the concrete blocker.
- **Wedell-Wedellsborg moves** (pick the most fitting): look outside the frame, rethink the goal, examine bright spots (when is the problem absent?), take another stakeholder's perspective.

One short exchange, no agent calls. The chosen framing becomes the contract objective.

### 0.2 Pruning contract

Lock, with the user:
- **Objective**: one sentence, the chosen framing.
- **Criteria**: 2 to 4 decidable pruning criteria (an idea either passes or fails each; "must not require user intervention" is decidable, "should be elegant" is not).
- **Anti-objective**: one sentence on what this problem is NOT.
- Optionally, criterion weights. Without them, the critic uses defaults (novelty 0.35, viability 0.40, fit 0.25).

If the user cannot state an objective, abort to a direct answer; a divergence without a contract is decoration.

### 0.3 Grounding brief

Harvest reality so branches do not rediscover the vault or ignore known constraints.

vault-mode:
```bash
obsidian search query="<theme terms>" limit=10
obsidian backlinks file="<closest existing note>"
obsidian tag name="<relevant tag>" verbose
```
Read the 3 to 8 most relevant notes and synthesize the brief with three sections, every item carrying its [[wikilink]] provenance:
- **FACTS**: what is known and decided.
- **CONSTRAINTS**: what limits the solution space.
- **BANLIST**: ideas that already exist in the vault (banned as "new"; branches may build on them only if structurally different, flagged as builds_on).

artifact-mode: same three sections harvested from the project documents in context, provenance by document name.

Discipline rule: the brief carries facts, constraints, and the banlist, never solution directions. Anchoring on facts is the grounding we want; anchoring on solutions is what the banlist exists to prevent. This is the deliberate trade-off against pure branch isolation, and it stays safe only while the brief stays direction-free.

## Phase 1: Diverge (no critic)

1. Pick 5 cognitive frames from the table below. For code-shaped problems: 4 tagged code/design plus 1 wild. For product/strategy: mix across tags. Vary picks across sessions.
2. Spawn 5 parallel, isolated calls to the **divergent-generator** agent. Each branch receives only: the problem (contract objective), the frame's vantage prompt, and the grounding brief. Branches never see each other; isolation is what prevents anchoring, do not serialize and do not share outputs between branches.
3. Each branch returns 6 ideas as JSON (text, rationale, optional builds_on).

### Frames

| Frame | Vantage prompt | Tags |
|---|---|---|
| hardware engineer | You think in latency, memory layout, physical constraints. Re-ask this as a hardware problem. | code, wild |
| regulator | You audit for compliance and failure modes. What must be provable, traceable, refusable? | design, general |
| 10-year-old | Curious child who never saw software. Naive but unencumbered approaches. Ignore convention. | general, wild |
| hostile competitor | Generate approaches that exploit, break, or sabotage the obvious solution; invert into ideas. | code, design |
| biology | Transplant a mechanism from biology (immune systems, plasticity, evolution) and force-fit it. | code, wild |
| logistics | Steal mechanisms: queues, batching, just-in-time, hub-and-spoke, last-mile. Apply literally. | code, design |
| game design | Loops, rewards, friction, save-states, speedrun tricks. Treat the user as a player. | design, general |
| markets | Buyers, sellers, market-makers. What does an auction or clearing house look like here? | design, wild |
| inversion | Ask the OPPOSITE question (how to guarantee NOT the goal), then negate each answer back. | code, design, general |
| $0 budget, 1 hour | Crudest version that still does the load-bearing thing. | code, general |
| infinite budget, 10 years | The maximalist version. | design, wild |
| remove the load-bearing assumption | Name what everyone treats as fixed; imagine it gone. | code, design, wild |
| speedrunner | Glitches, skips, frame-perfect shortcuts. The abusive-but-legal path. | code, wild |
| ant colony | No central planner: many dumb agents, local rules, pheromone trails. Emergent solution. | code, wild |
| 3am on-call | The design that never pages you. | code, design |

## Phase 2: Qualified pruning (critic on)

Invoke the **convergent-critic** agent once with: the contract, the full pool, the grounding brief. It runs four passes: score (novelty/viability/fit, contract-weighted), contract verdict (every cut cites the criterion that killed it; survivors checked against the anti-objective), traps (mechanistic reasons only), cluster and commit (3 to 6 angle clusters, 2 to 4 shortlist, non-obvious-but-viable pick starred).

Then deepen the top 3 (one call each, or reuse the critic): a 4 to 8 sentence sketch, the load-bearing risk, the first concrete step, 3 to 5 child ideas.

## Phase 3: Persist

vault-mode:
1. Synthesis note in `Atlas/` named `YYYY-MM-DD-divergence-<slug>.md`: objective, criteria, reframe chosen, shortlist with star, clusters, trap list, cut list with verdicts (conscious discard in batch), provocation, `connections` to every grounding source.
2. Each deepened top-K idea becomes its own note, `status: parking-lot`, `origin: divergence`, `connections` to sources and to the synthesis note. They enter the parking-lot flow: /converge and incubation review will see them.
3. Log line in `System/`.

```bash
obsidian create path="Atlas/2026-08-12-divergence-slug.md" content="..." silent
obsidian property:set name="status" value="parking-lot" path="Atlas/idea-note.md"
```

artifact-mode: one versioned artifact `current-divergence-<slug>.md` with the full synthesis, for the user to store in their project files (incremental versioning, replace on next run).

## Output shape (in the conversation)

1. Brief: problem + reframe used, two lines.
2. Wide set: clusters with score chips [N7 V8 F9].
3. Converge: shortlist with reasons, star pick, traps with reasons, cuts with contract verdicts.
4. Focus: the 3 deepened branches.
5. Provocation: one wildcard question.
6. Persistence receipt: what was written where.

## Anti-patterns

- Convergence disguised as divergence: ten variations of one idea is decoration, not breadth.
- Weird-for-weird's-sake with no convergence: always converge with a real opinion.
- Skipping isolation: sequential branches in one context are a wider single thought, not divergence.
- A direction-loaded grounding brief: the moment the brief suggests solutions, isolation is dead. Facts, constraints, banlist only.
- Contract theater: criteria that nothing could fail ("should be good") make the pruning unqualified. Criteria must be decidable.

## Calibration and cost

Default 5 frames x 6 ideas. Scale down (3 x 4) for naming-sized problems, up (5 x 8) for strategy. Stop diverging when new candidates repeat the shape of existing ones. Cost: 5 diverge + 1 critic + 3 deepen + grounding synthesis, ~10 to 12 calls. Not for every keystroke; for decision points where the obvious answer being wrong is expensive.
