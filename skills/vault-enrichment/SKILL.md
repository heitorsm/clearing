---
name: vault-enrichment
description: |
  Progressive enrichment of existing notes in an ACE + Zettelkasten Obsidian vault (Inbox, Atlas, Calendar, Efforts, Clippings, Work, Archive, System, 0.Templates, 1. General): adds frontmatter, tags, wikilink connections, type, and maturity. Vault health diagnostics with graph metrics via scan script. Operates via the Obsidian CLI (v1.12.7+). Use whenever the user mentions: enrich notes, enrich vault, add metadata, add tags, add frontmatter, orphan notes, notes without links, notes without tags, migrate notes, improve vault, vault health, loose notes, abandoned notes, vault scan, diagnose vault, how many notes, tag distribution, migration progress, enrichment, enriquecer notas, diagnosticar vault, notas órfãs, or any reference to improving the quality and connectivity of existing notes. Also on "organize my vault", "how are my notes", "what needs attention", "help me link". Vault-only: requires the Obsidian CLI on PATH and Obsidian running; this skill does not operate in artifact-mode and must say so instead of simulating.
---

# Vault Enrichment

Progressive enrichment of existing notes: frontmatter, tags, links, and classification for raw notes, turning an organic vault into a navigable knowledge graph. Aligned with obsidian-parking-lot: same folders, same schema, same CLI syntax. The two skills write to the same vault and must not diverge.

## Operating principle

Progressive enrichment beats big-bang reorganization: every note touched is re-encoded at a deeper processing level, and the system stays functional throughout. The agent never writes without explicit validation: propose, user approves, agent applies. Approval is per batch, item by item or in block.

This skill is **vault-only**. Without the Obsidian CLI there is no vault, no graph, and no honest version of enrichment; declare it in one line and stop, never simulate.

## Prerequisites

- Obsidian 1.12.7+ (dedicated CLI binary). After updating the app, re-register the CLI in Settings: General and validate with `obsidian version` and `obsidian vault`.
- Obsidian running (the CLI is a remote control).
- Full CLI syntax reference: `references/obsidian-cli.md` in this skill (read the file directly; no CLI needed). obsidian-parking-lot carries an identical copy; update both together.

Two syntax rules that cause immediate failure: subfolders require `path="Folder/note.md"`; property search requires brackets `[status:parking-lot]`.

## Vault context

```
Inbox/           Capture (owned by parking-lot; do not enrich here)
Atlas/           Permanent notes, MOCs
Calendar/        Daily notes (do not enrich)
Efforts/         Active projects
Clippings/       Articles (Web Clipper pattern)
Work/            Client work (write ONLY with explicit per-note confirmation)
Archive/         Archived
System/          Conventions, logs, scripts
0.Templates/     Native templates (exclude from every scan)
Lists/           Lists (low priority)
1. General/      Legacy knowledge base (~288 notes): MAIN TARGET of the migration
```

Destination for enriched `1. General/` notes: consolidated conceptual notes migrate to `Atlas/` via `obsidian move` (preserves wikilinks). Notes the user prefers to keep in place get their frontmatter where they are: enrichment never forces a move.

## Unified frontmatter schema

```yaml
---
Created: 2023-05-15          # required; creation date (file metadata when unknown)
Updated: 2026-08-12          # required; update on every enrichment
type: concept                 # required; concept|reference|literature|project|fleeting|moc
maturity: 🌿                 # required; 🌱 raw | 🌿 structured | 🌲 evergreen
status: archived              # optional; only when the note participates in the parking-lot flow
tags:                         # required; 3 to 5
  - marketing/retention
  - bridge
connections:                  # recommended; explicit wikilinks (native vault field)
  - "[[feedback-loops]]"
aliases:                      # optional; search-improving alternative titles
  - "Customer Lifetime Value"
project:                      # optional
origin: reading               # optional; quick-capture|meeting|reading|reflection|conversation|divergence
outcome:                      # optional; worked|failed|learned: <one line>, set when an active idea concludes
---
```

Alignment rules (never violate):
- Fields are `Created`, `Updated`, `connections`. NEVER write lowercase `created` or `related`: they create duplicate fields invisible to the vault's Dataview.
- `maturity` (🌱🌿🌲) and `status` (parking-lot flow: inbox, parking-lot, active, archived, discarded) are independent dimensions. Enrichment owns `maturity` and never changes an existing `status` without instruction.
- English values are canonical. Legacy Portuguese values (`ativo`, `arquivado`, `descartado-consciente`; categories `projetos`, `referências`, `explorar`; origins `leitura`, `reunião`...) are flagged by the scan as `legacy-values` and migrated to English whenever a note is touched.
- Clippings keep the Web Clipper fields as-is; add only `maturity`, `connections`, and thematic tags.

### Maturity criteria

| Maturity | Criterion |
|---|---|
| 🌱 | Raw, no links, fragmentary content |
| 🌿 | Structured, some links, usable content |
| 🌲 | Polished, well-linked, own synthesis, citable |

### Note types

| Type | Criterion |
|---|---|
| `concept` | Explains a concept, theory, or framework |
| `reference` | Points to an external source |
| `literature` | Reading note with quotes and summary of one source |
| `project` | Tied to a deliverable, client, or initiative |
| `fleeting` | Raw fragmentary capture |
| `moc` | Map of content organizing and linking other notes |

## Operations

### OP1: Vault Diagnostic

Trigger: "/diagnose", "diagnose vault", "vault health", "how are my notes", "quantas notas tenho".

1. Quick metrics via CLI: `obsidian files total`, `obsidian tags counts sort=count`, `obsidian files sort=modified limit=20`.
2. Deep scan via filesystem (the CLI is slow at scale): run `scan_vault.py` against the vault path (get it with `obsidian vault`). It classifies every note (orphan, stub, untagged, no-frontmatter, legacy-schema, legacy-values, enriched), computes graph metrics (in/out centrality, cross-domain bridge score, co-citation pairs, MOC-less cluster candidates), and produces the priority queue.
3. Report: totals and per-folder distribution, frontmatter and tag coverage, orphan percentage, maturity distribution, legacy values pending migration, top 20 priorities.
4. Save the snapshot to `System/diagnostic-log-YYYY-MM-DD.md` and suggest next steps.

### OP2: Batch Enrichment

Trigger: "/enrich", "enrich N notes", "process old notes", "add metadata", "enriquecer".

1. Select notes: user-specified, or top N by priority score (default 5).
2. Read each note in full. For 6+ notes with sub-agents available, parallelize analysis and consolidate.
3. Propose per note: `type`, `maturity`, 3 to 5 tags reusing the existing vocabulary (`obsidian tags counts`), 2 to 5 `connections` (mechanical lookups by the orchestrator; invoke the **relation-scout** agent only for deep semantic passes), `aliases` when they improve search, and legacy-value migration when flagged.
4. Present the whole batch for validation:
   ```
   ## [Note Name] (current folder)
   Content: [1-2 line synthesis]
   type: concept · maturity: 🌿
   tags: marketing/retention, data-science/metrics, bridge
   connections: [[churn-model]], [[feedback-loops]]
   migrate values: status ativo -> active
   move to: Atlas/ (or keep)
   ```
5. Apply approved changes via CLI, always with `path=`:
   ```bash
   # Note without frontmatter: prepend the full YAML block
   obsidian prepend path="1. General/Marketing/note.md" content="---\nCreated: 2023-05-15\nUpdated: 2026-08-12\ntype: concept\nmaturity: 🌿\ntags:\n  - marketing/retention\nconnections:\n  - '[[feedback-loops]]'\n---"

   # Note with frontmatter: property:set per field
   obsidian property:set name="type" value="concept" path="1. General/Marketing/note.md"
   obsidian property:set name="maturity" value="🌿" path="1. General/Marketing/note.md"
   obsidian property:set name="Updated" value="2026-08-12" path="1. General/Marketing/note.md"

   # Approved migration to Atlas
   obsidian move path="1. General/Marketing/note.md" to="Atlas/"
   ```
6. Batch summary to `System/enrichment-log-YYYY-MM-DD.md`: notes processed, new vs reused tags, links created, migrations.

### OP3: Single-Note Enrichment

Trigger: "enrich [note]", "add metadata to [note]".

Same as OP2 for one note. Useful when the user finds a note during normal use.

### OP4: Connection Suggestions

Trigger: "find missing links", "suggest connections", "link notes", "unlinked mentions".

Semantic judgment, not term matching. Read the batch in full (filesystem for large batches), infer relations through three lenses in order of value: second-order (A solves what B mentions, no shared vocabulary needed; these produce serendipity), bridge notes (universal concepts crossing domains; propose creating the bridge note when a cluster justifies it), direct thematic (sparingly; co-occurrence is noise). Confirm every proposed target exists (`obsidian search query="title" limit=3`); flag new-note proposals explicitly. Quality filter: complete "this connection matters because..." for each suggestion; if the honest answer is "both mention X", discard. Apply approved links to `connections` and, when natural in the text, as inline wikilinks via `obsidian append`.

### OP5: Progress Report

Trigger: "migration progress", "how is the enrichment", "vault status".

1. Run the scan (OP1 simplified).
2. Compare with the last `System/diagnostic-log-*.md`.
3. Report: notes enriched in the period, coverage before and after, orphan percentage before and after, average velocity (notes/week), completion projection, legacy values remaining.
4. Save the new snapshot to System/.

## Prioritization criteria

When the user does not specify notes:

1. Notes with inlinks but no frontmatter (high network value, low cost)
2. Substantive notes (>200 words) in `1. General/` without tags or links: the main migration corpus
3. Notes in `Efforts/` (immediate impact on active work)
4. Recent notes without metadata (context still fresh)
5. Old notes with informative titles

Notes under 50 words with no links are merge or discard candidates, not enrichment targets: flag them. Exception: notes carrying legacy schema or legacy values stay in the queue regardless of length; that migration is mechanical and always worth doing. `Calendar/`, `0.Templates/`, and `Lists/` stay out of the queue by default. `Work/` enters only on explicit request, and every write in `Work/` requires per-note confirmation.

## Tag vocabulary management

1. Before any new tag, check existing ones: `obsidian tags counts`. Prefer an existing tag with 3+ uses.
2. Check variants before creating (singular/plural, PT/EN).
3. Ceiling of ~100 tags for a vault up to 500 notes (cue overload).
4. Hierarchical for topics (`marketing/retention`), flat for functions (`bridge`, `to-process`, `seed`).
5. Duplicates found in the scan: propose consolidation via `obsidian tags:rename old="x" new="y"` (atomic across the vault).

## Script: scan_vault.py

Deep scan via direct filesystem (the CLI is slow in bulk). Ships with this skill and should also live at `System/Scripts/scan_vault.py` in the vault, versioned with the corpus.

Usage: `python3 scan_vault.py "/path/to/vault" [--json] [--output file]`

Excludes `.obsidian/`, `.trash/`, `0.Templates/`. Understands the unified schema (`Created`, `Updated`, `maturity`, `connections`), counts frontmatter `connections` as outlinks, flags `legacy-schema` (lowercase created / related fields) and `legacy-values` (Portuguese status/category/origin values), and computes graph metrics: in/out degree, cross-domain bridge score (distinct top-folders a note connects), co-citation pairs, and densely linked tag clusters without a MOC. These metrics feed both the priority queue and the /emerge analysis.

## Interaction with other skills

| Situation | Skill |
|---|---|
| Inbox note needs flow triage, not metadata | obsidian-parking-lot |
| A parking-lot note matured during enrichment | Flag it; promotion belongs to /converge |
| Graph metrics needed for emergence analysis | /emerge command (relation-scout agent) |

Parking-lot manages the flow of new ideas; enrichment migrates and improves the corpus. Same vault, same schema, identical bundled CLI reference (`references/obsidian-cli.md` in both skills).
