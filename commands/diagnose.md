---
description: Vault health diagnostic: coverage, orphans, maturity, graph metrics, priority queue (vault-enrichment OP1)
---

Run the vault diagnostic operation (OP1) of the vault-enrichment skill. Collect quick metrics via the Obsidian CLI (files total, tags counts, recently modified), then run the deep scan script (scan_vault.py) against the vault path for classification (orphan, stub, untagged, no-frontmatter, legacy-schema, legacy-values, enriched), graph metrics (centrality, cross-domain bridge scores, MOC-less cluster candidates), and the enrichment priority queue. Report totals, coverage percentages, maturity distribution, top priorities, and any legacy Portuguese values pending migration. Save the snapshot to System/ and suggest next steps.
