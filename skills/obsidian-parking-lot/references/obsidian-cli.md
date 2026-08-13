# Obsidian CLI Reference

Bundled reference for the Obsidian CLI, carried by both clearing skills (obsidian-parking-lot and vault-enrichment) as identical copies. Read this file directly from the skill folder: it does not require the CLI or Obsidian running. Maintenance: when the CLI changes syntax, update this file in both skills at once (same content).

Reference version: Obsidian 1.12.7+ (dedicated CLI binary). Full official reference: `obsidian help`.

## Setup and environment

- Since 1.12.7 the installer ships a dedicated CLI binary, replacing the old Electron-based method and making terminal interactions significantly faster. After updating Obsidian, re-register the CLI in Settings: General: Command line interface, open a new terminal, validate with `obsidian version` and `obsidian vault`.
- The CLI is a remote control for the app: Obsidian must be running. If it is not, the first command triggers the launch, but wait for startup to complete.
- Non-login shells (automations, AppleScript `do shell script`) may not load the user PATH. If `obsidian` does not resolve, export the binary path before calling.
- Multiple vaults: the CLI connects to the active vault. For another vault, pass `vault="Name"` on every command.
- Scale limitation: every command is a call to the app. Bulk processing (hundreds of files) should use the direct filesystem for reading and analysis (e.g. scan_vault.py), reserving the CLI for safe writes and index-dependent operations.

## Critical syntax rules

These two rules cause immediate failure when ignored:

1. **Subfolders require `path=`.** The `name=` parameter does NOT accept `/`. For any note outside the vault root, use `path="Folder/note.md"` (with extension). `file=` works only for names unique in the vault; with ambiguity or subfolders, `path=` is the only robust option.

2. **Property search requires brackets.** The bracket-less form returns `Error: Operator "status" not recognized`.
   - Correct: `[status:parking-lot]` or `["status":"parking-lot"]`
   - Wrong: `status:parking-lot`
   - Exclude a folder from results: `[status:parking-lot] -path:0.Templates`

## Read and search

```bash
obsidian read path="Atlas/note.md"
obsidian read file="unique-name-in-vault"
obsidian search query="term" limit=20
obsidian search query="term" format=json
obsidian search:context query="term" limit=10
obsidian search query='[status:parking-lot] -path:0.Templates' format=json
obsidian files total
obsidian files sort=modified limit=10
obsidian files format=json
obsidian backlinks file="note-name"
obsidian file file="note-name"          # note metadata
obsidian folders                         # folder tree
```

## Create and edit

```bash
obsidian create path="Inbox/2026-08-12-idea.md" content="# Idea" silent
obsidian create path="Inbox/2026-08-12-idea.md" template="PL - Capture" silent
obsidian append path="Inbox/2026-08-12-idea.md" content="\n## Section\nContent"
obsidian prepend path="Inbox/2026-08-12-idea.md" content="Top line"
```

`silent` avoids opening the note in the app. Templates resolve from the vault's configured templates folder (`0.Templates/`).

## Properties (frontmatter)

```bash
obsidian property:set name="status" value="parking-lot" path="Atlas/note.md"
obsidian property:set name="Updated" value="2026-08-12" path="Atlas/note.md"
obsidian properties path="Atlas/note.md"
obsidian properties path="Atlas/note.md" format=json
```

`property:set` is the safe way to manipulate YAML. For list fields (tags, connections, aliases), when `property:set` does not support the desired structure, edit the YAML block via read plus surgical rewrite, preserving all other fields.

## Move and delete

```bash
obsidian move path="Inbox/idea.md" to="Atlas/"
obsidian delete path="Atlas/idea.md"
```

`obsidian move` updates every wikilink in the vault. NEVER use system `mv` to move notes: it silently breaks links. The CLI has no directory command: use `mkdir -p` on the filesystem.

## Tags

```bash
obsidian tags counts sort=count
obsidian tag name="architecture" verbose
obsidian tags:rename old="old-tag" new="new-tag"
```

`tags:rename` is atomic across the vault.

## Daily notes

```bash
obsidian daily:read
obsidian daily:append content="- [ ] Triage Inbox"
```

## Utilities

```bash
obsidian vault
obsidian version
obsidian eval code="app.vault.getFiles().length"
```

`obsidian eval` runs JavaScript in the app context: useful for queries the CLI does not cover, use sparingly.

## CLI vs filesystem: quick decision

| Scenario | Use |
|---|---|
| Move a note | `obsidian move` (preserves wikilinks) |
| Create a note | `obsidian create silent` (native templates) |
| Search by content or property | `obsidian search` (index) |
| Read 1 note | `obsidian read` |
| Read hundreds of notes (scan, analysis) | Direct filesystem (Python/bash) |
| Edit frontmatter | `obsidian property:set` |
| Backlinks and graph | `obsidian backlinks` |
| Create a directory | `mkdir -p` |
