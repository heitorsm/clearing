---
description: Enrich a batch of notes: frontmatter, tags, connections, type, maturity (vault-enrichment OP2)
argument-hint: [count or note names, default 5]
---

Run the batch enrichment operation (OP2) of the vault-enrichment skill on: $ARGUMENTS (default: top 5 by priority score). For each note, read the full content and propose type, maturity, 3 to 5 tags reusing the existing vocabulary, 2 to 5 connections (mechanical lookups by the orchestrator; invoke the relation-scout agent only for deep semantic passes), and aliases when they improve search. Present the whole batch for validation, then apply approved changes via the Obsidian CLI using path= syntax, migrating any legacy fields or Portuguese values to the unified English schema. Summarize the batch in System/.
