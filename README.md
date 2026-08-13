# clearing

Cultivate divergent tree-thinking in your Obsidian vault, then prune to clarity.

clearing is a Claude Code / Cowork plugin that operationalizes the journey of the [Design Squiggle](https://thedesignsquiggle.com): from hyperassociative noise on the left to clarity and focus on the right. It treats branching, hyperassociative thinking as a feature to be cultivated, not a bug to be suppressed, and pairs it with the three things divergence needs to produce value instead of noise: **clarity of sources, explicit connections, and a declared objective that enables qualified pruning**.

The name: a clearing is what you reach after walking through dense forest, and opening a clearing is literally pruning. The forest (your branching thought, your vault) is the terrain; the clearing is where you can finally see.

## What it delivers

The full divergence-convergence cycle of the Double Diamond, grounded in a personal knowledge vault:


| Double Diamond                    | clearing                                                                                                                                       |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Discover / Define (problem space) | Phase 0 of /diverge: Reframe (abstraction laddering, Wedell-Wedellsborg moves) + pruning contract + grounding brief harvested from the vault   |
| Develop (solution divergence)     | Phase 1: N parallel isolated branches under cognitive frames, generator only, evaluation forbidden                                             |
| Deliver (solution convergence)    | Phase 2: qualified pruning against the contract, per-criterion verdicts, trap detection; Phase 3: persistence into the vault                   |
| The engine around the diamonds    | Capture (/triage flow), incubation (/converge), corpus health (/diagnose, /enrich), and system-level emergence (/emerge, Donella Meadows lens) |




## Requirements

- Claude Code or Claude Cowork (plugins are not installable on claude.ai web; see Modes below).
- For the full experience (vault-mode): Obsidian 1.12.7+ with the CLI registered (Settings: General: Command line interface) and Obsidian running. Validate with `obsidian version` and `obsidian vault`.
- A vault following the ACE + Zettelkasten layout (Inbox, Atlas, Calendar, Efforts, Clippings, Work, Archive, System, 0.Templates). Other layouts work with minor edits to the skills' folder maps.



## Install

Claude Code, from a local clone:

```bash
git clone https://github.com/heitormiranda/clearing.git
claude plugin install ./clearing
```

Or add the repo as a marketplace source and install from there. Cowork consumes the same plugin directory. After install, the six slash commands and three skills are available; the agents are invoked by the skills, never directly by you.

claude.ai web cannot install plugins: zip the individual skill folders (`skills/obsidian-parking-lot/`, `skills/vault-diverge/`) and upload via Settings > Skills. They will run in artifact-mode there (see Modes).

## Quickstart

```
/diagnose            # first contact: vault health, graph metrics, priority queue
/triage              # empty your Inbox with assisted classification
/diverge             # how should we structure the pricing model for X?
/converge            # weekly: what is ripe, what is decaying
/emerge              # monthly: leverage points and emergent structures
```



## The choreography

The Squiggle is not linear and neither is your week. This is when to be in which mode:

```
 noise ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~> clarity

 capture          triage         diverge        converge        act
 (any moment)     (daily-ish)    (decision      (weekly)        (Efforts/)
                                  points)
 Inbox/           status:        contract +     promote /       status:
 status: inbox    parking-lot    branches +     incubate /      active
                                  pruning        archive         ... outcome
                        \______________________________/
                          enrich + emerge run underneath
                          (corpus health and system-level sight)
```

- **Capture** costs nothing and asks nothing: never categorize at capture time.
- **Triage** is where organization happens, with assistance, in batch.
- **Diverge** is expensive (~12 agent calls) and gated: use it at decision points where the obvious answer being wrong is costly. It always starts by challenging the question itself (Reframe) before generating answers.
- **Converge** is the harvest ritual: clusters, maturity, decay, and a committed opinion per cluster.
- **Emerge** is the systems-thinking ritual (Meadows): leverage points, feedback loops, self-organizing clusters, silent domains. It looks at the vault as a system, not as notes.
- **Enrich / Diagnose** keep the corpus healthy so grounding and connections stay trustworthy.



## Commands


| Command              | What it does                                    | Skill behind it          |
| -------------------- | ----------------------------------------------- | ------------------------ |
| /diverge [problem]   | Full grounded divergence session, gate bypassed | vault-diverge            |
| /triage              | Inbox triage: classify, tag, connect, file      | obsidian-parking-lot OP2 |
| /converge            | Periodic convergence: clusters, maturity, decay | obsidian-parking-lot OP4 |
| /diagnose            | Vault health + graph metrics + priority queue   | vault-enrichment OP1     |
| /enrich [n or notes] | Batch metadata enrichment                       | vault-enrichment OP2     |
| /emerge              | Leverage points, loops, emergent clusters       | scan + relation-scout    |




## Skills

- **vault-diverge**: the 4-phase loop (Anchor with Reframe, Diverge, Qualified Pruning, Persist). Adapted from the MIT-licensed [adhd](https://github.com/UditAkhourii/adhd) skill by UditAkhouri, with three structural additions: source grounding from the vault, a pruning contract with per-criterion verdicts, and persistence into the incubation flow.
- **obsidian-parking-lot**: capture, triage, connection analysis, periodic convergence, incubation review. Lifecycle by frontmatter status, notes live in semantic folders.
- **vault-enrichment**: progressive enrichment of the legacy corpus, tag vocabulary management, deep scan with graph metrics. Vault-only.



## Agents

Three postures, mechanically separated (the load-bearing design choice inherited from the adhd skill: generator and critic as different calls with opposite system prompts, never one model promising to do both):

- **divergent-generator**: pure generation, evaluation forbidden, obvious-first-three banned, banlist-aware.
- **relation-scout**: semantic connections (second-order, bridge notes) with a mandatory quality filter, plus the emergence lens for /emerge. Gated: mechanical lookups (backlinks, shared tags) are handled by the orchestrator with two CLI calls; the scout is invoked only for judgment.
- **convergent-critic**: mandatory evaluation against the Phase 0 contract, per-criterion verdict for every cut, traps with mechanistic reasons, cluster and commit with a starred non-obvious-but-viable pick.



## Example walkthroughs

**Capture** (friction zero):

> you: tive uma ideia: usar o padrão de circuit breaker no orquestrador de agentes
>
> claude: Captured as `Inbox/2026-08-12-circuit-breaker-orquestrador.md`. It will wait for the next /triage.

**Diverge** (compressed):

> you: /diverge how do we keep NBA decisioning explainable for the bank's audit team?
>
> claude: **Mode: vault-mode.** Before locking the contract, three framings: (1) as stated; (2) laddered up: how do we make the audit team trust automated decisions?; (3) bright spot: what already passes audit today and why? Pick one.
>
> you: 2
>
> claude: Contract: objective = audit team trusts automated NBA decisions. Criteria: C1 every decision reproducible from logged inputs; C2 no explanation requires ML literacy; C3 works within current data retention policy. Anti-objective: this is not about improving model accuracy. Grounding brief from [[nba-architecture]], [[audit-2025-findings]], [[decision-logs]]: 4 facts, 2 constraints, banlist of 3 existing ideas.
> [5 branches: regulator, inversion, 10-year-old, logistics, 3am on-call]
> Wide set: 27 ideas in 5 clusters ... Cuts include "post-hoc SHAP dashboards" (fails C2, requires ML literacy). ★ non-obvious pick: decision passports (each decision ships with its own replayable evidence bundle) ...
> Persisted: `Atlas/2026-08-12-divergence-nba-auditability.md` + 3 idea notes entering the parking lot.

**Emerge** (compressed):

> you: /emerge
>
> claude: Leverage points: [[feedback-loops]] bridges 4 domains with 11 links; enriching it reorganizes marketing, engineering, and biology clusters at once. Mutual-citation loop: [[mmm-priors]] <-> [[bayesian-calibration]], amplifying each other with no third connection: consider a bridge. MOC-less cluster: #cdp with 9 notes and no map: proposed MOC, "What does identity resolution actually decide?". Silent domain: `Lists/` has volume, zero bridges (expected). Synthesis persisted to Atlas/ on your approval.



## Data contract

Unified frontmatter schema (English values are canonical):

```yaml
Created: 2026-08-12        # never lowercase "created"
Updated: 2026-08-12
type: concept              # concept|reference|literature|project|fleeting|moc
maturity: 🌿              # 🌱 raw | 🌿 structured | 🌲 evergreen (owned by enrichment)
status: parking-lot        # inbox|parking-lot|active|archived|discarded (owned by parking-lot)
category: insights         # projects|insights|references|explore
origin: divergence         # quick-capture|meeting|reading|reflection|conversation|divergence
energy: high               # high|medium|low
tags: [marketing/retention, bridge]
connections: ["[[feedback-loops]]"]   # never "related"
outcome: "worked: shipped in Q3"      # closes the learning loop on concluded ideas
```

Legacy migration: older notes may carry Portuguese values (`ativo`, `arquivado`, `descartado-consciente`, `projetos`, `referências`, `explorar`, `leitura`...) or legacy fields (lowercase `created`, `related`). The scan flags them (`legacy-values`, `legacy-schema`) and /enrich migrates them whenever a note is touched. Reading is tolerant; writing is always English.

## Modes

- **vault-mode**: Obsidian CLI available. Full experience: grounding from the vault, wikilink persistence, Dataview surfacing, graph metrics.
- **artifact-mode**: no CLI (Cowork project without local Obsidian, claude.ai). vault-diverge runs nearly complete (grounding from project documents, output as a versioned `current-divergence-<slug>.md` artifact). parking-lot runs a triage/convergence subset over an inbox document. vault-enrichment does not operate and says so. The mode is detected and announced once per session; degradation is always declared, never simulated.



## Non-goals

Deliberate exclusions, so the plugin stays a thinking tool and does not become a product-team pipeline:

- No stakeholder share-out rituals (Kickoff/Inception ceremonies). The only gate that matters solo is check 4 of the pre-flight: is this problem validated?
- No Build & Learn delivery pipeline (prototyping, KPI tracking, experiment management). The single concession is the `outcome` frontmatter field, closing the learning loop in one line.



## Cost

/diverge is ~10 to 12 agent calls (5 to 10x a single answer) and is gated accordingly. /emerge is one scan plus one agent call. Everything else is CLI-bound and cheap.

## References

- Damien Newman, The Design Squiggle
- British Design Council, the Double Diamond (2005) and Framework for Innovation (2019)
- Thomas Wedell-Wedellsborg, "Are You Solving the Right Problems?" (HBR, 2017); What's Your Problem? (2020)
- Donella H. Meadows, "Leverage Points: Places to Intervene in a System" (1999); Thinking in Systems
- Cliff Guren, "Choreographing Creative Thinking"
- Bouschery, Blazevic & Piller, "Augmenting human innovation teams with artificial intelligence" (JPIM, 2023): the AI-augmented Double Diamond
- UditAkhouri, adhd (MIT): the parallel isolated divergence loop this plugin's Phase 1 descends from
- Nick Milo (ACE, MOCs), Andy Matuschak (evergreen notes), Sönke Ahrens (Zettelkasten)



## Troubleshooting

- `obsidian: command not found`: re-register the CLI (Settings: General), open a new terminal. In non-login shells, export the binary path.
- `Error: Operator "status" not recognized`: property searches need brackets: `[status:parking-lot]`.
- Notes not found by name: subfolder notes require `path="Folder/note.md"`; `name=` does not accept `/`.
- Broken wikilinks after a move: something used system `mv`. Always `obsidian move`.
- Slow bulk operations: the CLI is one app call per command; use `scan_vault.py` for analysis at scale.



## License

MIT. Phase 1 of vault-diverge descends from the MIT-licensed adhd skill by UditAkhouri; the frame library and the generator/critic mechanical split are credited to that work.