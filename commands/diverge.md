---
description: Run a full grounded divergence session on a problem (vault-diverge skill, pre-flight gate bypassed)
argument-hint: [problem statement]
---

The user explicitly invoked /diverge. Load and run the vault-diverge skill on the problem below, skipping the pre-flight self-judge (explicit invocation is opt-in). Run all phases: Phase 0 Anchor (Reframe, then pruning contract, then grounding brief), Phase 1 Diverge (parallel isolated branches via the divergent-generator agent), Phase 2 Qualified Pruning (convergent-critic agent), Phase 3 Persist (vault-mode or artifact-mode as detected).

Problem: $ARGUMENTS

If no problem was provided, ask for it in one line before starting.
