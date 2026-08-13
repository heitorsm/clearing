---
name: obsidian-parking-lot
description: |
  Idea and divergent-thinking management over an Obsidian vault via the Obsidian CLI (v1.12.7+), adapted to an ACE + Zettelkasten vault (Inbox, Atlas, Calendar, Efforts, Clippings, Archive, System, 0.Templates), with the parking-lot lifecycle governed by frontmatter (status). Runs 5 operations: capture, status-driven triage (Inbox captures and Clippings alike), connection analysis, periodic convergence, incubation review. Use when the user mentions: parking lot, inbox, triage notes, process inbox, triage clippings, review parking lot, converge ideas, analyze connections, clean inbox, organize vault, capture idea, what is in my inbox, incubate ideas, loose notes, cognitive backlog, triar, convergir, capturar ideia, "tive uma ideia", "preciso anotar isso", "o que eu estava pensando sobre X", "quais padrões estão aparecendo". Requires the Obsidian CLI on PATH and Obsidian running (vault-mode); degrades to a limited artifact-mode on project documents.
---

# Obsidian Parking Lot

Capture, triage, and convergence of ideas over an Obsidian vault via the Obsidian CLI. The note lives in the folder that matches its meaning; the parking-lot stage lives in frontmatter (`status`).

## Purpose

Manage the flow of divergent thinking: capture without friction, organize with assistance, converge periodically to turn ideas into action. The vault is a personal knowledge graph where the value lives in the connections between notes, not in isolated notes.

## Modes

- **vault-mode** (default): `obsidian version` responds and `obsidian vault` confirms the active vault. Full experience.
- **artifact-mode**: no CLI available (Cowork or claude.ai project context). Only a subset operates: triage and convergence over an inbox document provided in context, output as versioned artifacts. No friction-zero capture, no Dataview surfacing, no automatic incubation. Announce the mode once; never simulate vault features.

## Prerequisites (vault-mode)

- Obsidian 1.12.7+ with the dedicated CLI binary. After updating the app, re-register the CLI in Settings: General, open a new terminal, validate with `obsidian version` and `obsidian vault`.
- Non-login shells (automations, AppleScript `do shell script`) may not load the user PATH: export the binary path before calling if `obsidian` does not resolve.
- Obsidian must be running (the CLI is a remote control for the app).
- Full CLI syntax reference: `references/obsidian-cli.md` in this skill. Read the file directly (no CLI needed). The vault-enrichment skill carries an identical copy; update both together.

Two syntax rules that cause immediate failure (details in the reference):
1. Subfolders require `path="Folder/note.md"` with extension. The `name=` parameter does not accept `/`.
2. Property search requires brackets: `[status:parking-lot]`. Without brackets the CLI returns `Error: Operator "status" not recognized`. Exclude templates: `[status:parking-lot] -path:0.Templates`.

Tooling rule: the CLI is the preferred interface. NEVER use system `mv` to move notes (it breaks wikilinks; `obsidian move` preserves them). Direct filesystem only for creating directories (`mkdir -p`) and for bulk reads in analysis (the CLI is slow at hundreds of files).

## Vault layout (ACE + Zettelkasten)

Principle: no parallel `00-inbox/01-parking-lot/` tree. The category defines the semantic destination folder; `status` in frontmatter defines the stage. Surfacing via Dataview.

```
<vault-root>/
├── Inbox/           Raw capture, status: inbox
├── Atlas/           Insights, permanent notes, MOCs, branches to explore
├── Calendar/        Daily and periodic notes
├── Efforts/         Active projects (project parking-lot and status: active)
├── Clippings/       Articles and references (Web Clipper)
├── Work/            Client work (Clientes/<client>/); write only with explicit confirmation
├── Archive/         Archived and conscious discards
├── System/          Conventions, logs, scripts
├── 0.Templates/     Native templates (PL - Capture, PL - Triaged Note)
├── Lists/           Lists
└── 1. General/      Legacy knowledge base (migration owned by vault-enrichment)
```

## Status taxonomy (frontmatter)

```
inbox -> parking-lot -> active -> archived
                    \-> discarded -> archived
```

| Status | Typical folder | Meaning |
|---|---|---|
| `inbox` | Inbox/, Clippings/ | Raw capture or fresh clipping, unprocessed |
| `parking-lot` | Clippings/, Atlas/, Efforts/ | Triaged, categorized, awaiting action or incubating |
| `active` | Efforts/ | Promoted to concrete action |
| `archived` | Archive/ | Long-term reference |
| `discarded` | Archive/ | Evaluated and consciously let go (with `reason`) |

Legacy Portuguese values may exist in older notes (`ativo`, `arquivado`, `descartado-consciente`). Read them as their English equivalents; migrate them to English whenever you touch a note. The vault-enrichment scan flags them as `legacy-values`.

## Categories

| Category | Destination | Criterion |
|---|---|---|
| `projects` | Efforts/ or Work/Clientes/<client>/ | Tied to a project, client, or deliverable |
| `insights` | Atlas/ | Connection, pattern, or reflection with no project yet |
| `references` | Clippings/ | Consultation material: article, technique, tool |
| `explore` | Atlas/ | Thinking branch worth deepening |

## Frontmatter schema (unified)

Native vault fields: `Created`, `Updated`, `tags`, `connections`, `project`. Clippings keep the Web Clipper pattern (`title`, `source`, `author`, `published`, `created`, `description`, `tags: [clippings]`).

| Field | Type | Values | When |
|---|---|---|---|
| `Created` | date | YYYY-MM-DD | Always (capture) |
| `Updated` | date | YYYY-MM-DD | Every relevant edit |
| `status` | string | inbox, parking-lot, active, archived, discarded | Always |
| `category` | string | projects, insights, references, explore | After triage |
| `triaged` | date | YYYY-MM-DD | After triage |
| `origin` | string | quick-capture, meeting, reading, reflection, conversation, divergence | Optional |
| `tags` | list | Free tags | Optional |
| `connections` | list | Wikilinks | After triage |
| `project` | string | Project or client | When applicable |
| `energy` | string | high, medium, low | Optional |
| `promoted_to` | string | Destination path | When promoted |
| `reason` | string | Discard reason | When discarded |
| `outcome` | string | worked, failed, learned: <one line> | When an active idea concludes; closes the learning loop |
| `maturity` | string | 🌱 🌿 🌲 | Owned by vault-enrichment; triage does not set it |

Naming: idea notes `YYYY-MM-DD-descriptive-slug`; Clippings keep the article title; wikilinks `[[note-name]]` or `[[note-name|alias]]`; tags lowercase, no accents, hyphenated (`#data-engineering`).

## Templates

In `0.Templates/`, used by `obsidian create template=X`. On first run, create them if missing (older Portuguese templates PL - Captura / PL - Nota Triada may coexist until manually removed).

### PL - Capture

```markdown
---
Created: "{{date}}"
Updated: "{{date}}"
status: inbox
origin: quick-capture
tags: []
connections: []
---

{{content}}
```

### PL - Triaged Note

```markdown
---
Created: "{{original_date}}"
Updated: "{{date}}"
triaged: "{{date}}"
status: parking-lot
category: "{{category}}"
origin: "{{origin}}"
energy: "{{energy}}"
tags: []
connections: []
project:
---

## Context

## Core Idea

## Connections

## Next Step
```

### Web Clipper template (one-time user setup, recommended)

Configure the Obsidian Web Clipper template to include `status: inbox` in the frontmatter of every clip. New clippings then enter the triage queue automatically via the primary status search, with no backfill pass needed.

Logs go to `System/` as `triage-log-YYYY-MM-DD.md` and `convergence-log-YYYY-MM-DD.md` (summary, notes processed, patterns observed).

## Operations

### OP1: Assisted Capture

Trigger: "tive uma ideia", "I have an idea", "note this down", "capture".

1. Receive the content (unstructured is expected).
2. Generate a descriptive slug.
3. Create in Inbox/:
   ```bash
   obsidian create path="Inbox/YYYY-MM-DD-slug.md" template="PL - Capture" silent
   ```
   or inline with `content=`.
4. If the user mentioned relational context, include it in the body.
5. Confirm briefly with the file name.

Rule: never ask for categorization at capture time. Organization happens at triage.

### OP2: Triage (status-driven: Inbox captures and Clippings alike)

Trigger: "/triage", "triage inbox", "triage clippings", "process inbox", "what is in my inbox", "triar inbox".

The queue is status-driven, not folder-driven, honoring the vault principle that stage lives in frontmatter.

1. Build the queue in two passes:
   - **Primary**: `obsidian search query='[status:inbox] -path:0.Templates' format=json`. Any folder qualifies: Inbox/ captures and status-tagged clippings enter the same queue.
   - **Clippings backfill**: list `path:Clippings`, check properties, and include notes with NO `status` field (clipped before the status convention). Cap the backfill at 10 per session and say so when there are more.
2. For each note, read with `obsidian read` and propose: category (projects, insights, references, explore), tags grounded in `obsidian tags counts`, connections (mechanical lookups via `obsidian search`/`obsidian backlinks`; invoke the relation-scout agent only for deep semantic passes), and a next step. With 6+ notes and sub-agents available, parallelize analysis and consolidate into one review.
3. Present proposals note by note; the user validates, edits, or discards.
4. Apply per note type:

   **Idea notes** (from Inbox/):
   ```bash
   obsidian property:set name="status" value="parking-lot" path="Inbox/note.md"
   obsidian property:set name="triaged" value="YYYY-MM-DD" path="Inbox/note.md"
   obsidian property:set name="category" value="insights" path="Inbox/note.md"
   ```
   Restructure the body with the triaged template and move preserving wikilinks:
   ```bash
   obsidian move path="Inbox/note.md" to="Atlas/"      # insights or explore
   obsidian move path="Inbox/note.md" to="Clippings/"  # references
   obsidian move path="Inbox/note.md" to="Efforts/"    # projects
   ```

   **Clippings** (notes in Clippings/ or carrying Web Clipper fields):
   - NEVER apply the triaged-note template and NEVER overwrite Clipper fields (title, source, author, published, description).
   - The note is NOT moved: Clippings/ is already the semantic destination for references. Triage is in place:
   ```bash
   obsidian property:set name="status" value="parking-lot" path="Clippings/article-title.md"
   obsidian property:set name="triaged" value="YYYY-MM-DD" path="Clippings/article-title.md"
   obsidian property:set name="category" value="references" path="Clippings/article-title.md"
   ```
   Add thematic tags and connections via property edits or `obsidian append`.
   - **The key clipping question: does it spawn a derived note?** If the user has their own insight about the article, create a separate idea note (Inbox/ if raw, Atlas/ if already shaped) connected to the clipping via `connections`. Literature in, permanent notes out.
   - Optionally append a `## My take` section with the user's one-liner.
5. Discards (both types):
   ```bash
   obsidian property:set name="status" value="discarded" path="Clippings/note.md"
   obsidian property:set name="reason" value="one-line reason" path="Clippings/note.md"
   obsidian move path="Clippings/note.md" to="Archive/"
   ```
6. Write the triage log to System/.

On connections: propose what a careful reader would propose. Term co-occurrence without conceptual relation is noise.

### OP3: Connection Analysis

Trigger: "analyze connections", "what connects to X", "find patterns", "quais notas falam sobre Y".

1. Start from a theme, project, or note.
2. Gather: `obsidian backlinks` (existing links), `obsidian tag name="t" verbose` (shared tags), `obsidian search` and `obsidian search:context` (semantic), `obsidian files sort=modified` (temporal).
3. Present a connection map with direct, thematic, and second-order relations. Second-order connections (A to B to C where A and C never link directly) are the highest value of this operation.
4. Suggest new links (field `connections`); insert on approval via `obsidian append` or `obsidian property:set`.

### OP4: Periodic Convergence

Trigger: "/converge", "converge", "review parking lot", "what is ripe", "colheita".

1. Collect: `obsidian search query='[status:parking-lot] -path:0.Templates' format=json`
2. Read content and properties per note; invoke the **convergent-critic** agent for the three dimensions: thematic clusters, maturity (multiple backlinks, recent references, clear next step), decay (30+ days without modification or new connections).
3. Report per cluster: notes, synthesis, committed suggestion (promote, keep incubating, archive).
4. Promotions on approval:
   ```bash
   obsidian property:set name="status" value="active" path="Atlas/note.md"
   obsidian move path="Atlas/note.md" to="Efforts/"
   ```
5. Never discard automatically; archive candidates come with reasons and "keep" is always valid. Log to System/.

When an `active` idea concludes (the user reports it shipped, failed, or taught something), set `outcome` in one line. Incubation review uses this history.

### OP5: Incubation Review

Trigger: "what was I thinking about X", "revisit", "reabrir", "ideias sobre Y".

1. Search: `obsidian search query="theme"` and `obsidian search:context query="theme"`.
2. Read full content and properties of hits.
3. Reconstruct the thinking chain chronologically, including any `outcome` history.
4. Present the state: started with A, connected to B, last note was C, N days ago.
5. Ask: add a new note to the chain, promote something, archive the chain, or just recall.

## Dataview surfacing

Open parking lot:

```dataview
TABLE category, energy, triaged, file.folder AS folder
FROM "Clippings" OR "Atlas" OR "Efforts" OR "Inbox"
WHERE status = "parking-lot"
SORT triaged DESC
```

Triage queue (status-driven):

```dataview
LIST
WHERE status = "inbox"
SORT file.ctime DESC
```

Unprocessed clippings (no status yet):

```dataview
LIST
FROM "Clippings"
WHERE !status
SORT file.ctime DESC
```

Convergence candidates (parked 30+ days):

```dataview
TABLE (date(today) - date(triaged)).day AS "days parked"
WHERE status = "parking-lot" AND date(triaged) < date(today) - dur(30 days)
SORT triaged ASC
```

## Write scope

Reading for connection search is allowed across the whole vault. Writing happens in the managed folders (Inbox, Atlas, Clippings, Efforts, Archive, System). Never modify client notes in `Work/` without explicit confirmation. Metadata enrichment of the legacy corpus (`1. General/`) is owned by the vault-enrichment skill, which shares this schema and an identical bundled CLI reference.
