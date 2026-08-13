#!/usr/bin/env python3
"""
Vault Scanner (clearing): health diagnostics + graph metrics for an
ACE + Zettelkasten Obsidian vault.

Usage:
    python3 scan_vault.py "/path/to/vault" [--json] [--output report.md]

Aligned with the clearing unified schema:
- Fields: Created, Updated, type, maturity, status, tags, connections, aliases, outcome
- Excludes: .obsidian/, .trash/, 0.Templates/
- Frontmatter connections count as outlinks
- Flags legacy-schema (lowercase created / related) and legacy-values
  (Portuguese status/category/origin values) for migration
- Graph metrics: in/out degree, cross-domain bridge score, mutual-citation
  pairs, MOC-less cluster candidates (feeds /diagnose and /emerge)
"""

import os
import re
import json
import sys
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict

IGNORE_DIRS = {'.obsidian', '.trash', '0.Templates', 'node_modules', '.git'}
LOW_PRIORITY_FOLDERS = {'Calendar', 'Lists'}
MAIN_TARGET_FOLDER = '1. General'
ACTIVE_FOLDER = 'Efforts'

LEGACY_VALUES = {
    'status': {'ativo': 'active', 'arquivado': 'archived',
               'descartado-consciente': 'discarded'},
    'category': {'projetos': 'projects', 'referências': 'references',
                 'referencias': 'references', 'explorar': 'explore'},
    'origin': {'captura-rápida': 'quick-capture', 'captura-rapida': 'quick-capture',
               'reunião': 'meeting', 'reuniao': 'meeting', 'leitura': 'reading',
               'reflexão': 'reflection', 'reflexao': 'reflection',
               'conversa': 'conversation'},
    'energy': {'alta': 'high', 'média': 'medium', 'media': 'medium', 'baixa': 'low'},
}

FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n?', re.DOTALL)
WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]+)?\]\]')
TAG_INLINE_RE = re.compile(r'(?:^|\s)#([a-zA-Z][\w/-]*)', re.MULTILINE)
YAML_LIST_RE = r'^{field}:\s*\n((?:\s+-\s+.*\n?)*)'
YAML_INLINE_LIST_RE = r'^{field}:\s*\[([^\]]*)\]'
YAML_SCALAR_RE = r'^{field}:\s*(.+)$'
MATURITY_VALUES = {'🌱', '🌿', '🌲'}


def _extract_list(fm_text, field):
    items = []
    block = re.search(YAML_LIST_RE.format(field=field), fm_text, re.MULTILINE)
    if block:
        for line in block.group(1).strip().split('\n'):
            v = line.strip().lstrip('- ').strip().strip('"').strip("'")
            if v:
                items.append(v)
    inline = re.search(YAML_INLINE_LIST_RE.format(field=field), fm_text, re.MULTILINE)
    if inline:
        for v in inline.group(1).split(','):
            v = v.strip().strip('"').strip("'")
            if v:
                items.append(v)
    return items


def _extract_scalar(fm_text, field):
    m = re.search(YAML_SCALAR_RE.format(field=field), fm_text, re.MULTILINE)
    if not m:
        return None
    v = m.group(1).strip().strip('"').strip("'")
    return v or None


def parse_frontmatter(content):
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None
    fm = match.group(1)
    legacy_hits = []
    for field, mapping in LEGACY_VALUES.items():
        val = _extract_scalar(fm, field)
        if val and val.lower() in mapping:
            legacy_hits.append(f"{field}: {val} -> {mapping[val.lower()]}")
    return {
        'tags': _extract_list(fm, 'tags'),
        'connections': _extract_list(fm, 'connections'),
        'legacy_related': _extract_list(fm, 'related'),
        'type': _extract_scalar(fm, 'type'),
        'maturity': _extract_scalar(fm, 'maturity'),
        'status': _extract_scalar(fm, 'status'),
        'outcome': _extract_scalar(fm, 'outcome'),
        'created': _extract_scalar(fm, 'Created') or _extract_scalar(fm, 'created'),
        'has_legacy_created': bool(re.search(r'^created:', fm, re.MULTILINE)),
        'legacy_values': legacy_hits,
    }


def analyze_note(filepath, vault_root):
    rel_path = os.path.relpath(filepath, vault_root)
    name = Path(filepath).stem
    top_folder = rel_path.split(os.sep)[0] if os.sep in rel_path else '(root)'

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception:
        return None

    fm = parse_frontmatter(content)
    body = FRONTMATTER_RE.sub('', content)
    word_count = len(body.split())

    body_links = set(WIKILINK_RE.findall(body))
    fm_links = set()
    if fm:
        for c in fm['connections'] + fm['legacy_related']:
            m = WIKILINK_RE.search(c)
            fm_links.add(m.group(1) if m else c)
    outlinks = sorted({l.strip() for l in (body_links | fm_links) if l.strip()})

    inline_tags = set(TAG_INLINE_RE.findall(body))
    fm_tags = set(fm['tags']) if fm else set()
    all_tags = sorted(fm_tags | inline_tags)

    try:
        mod_date = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')
    except Exception:
        mod_date = None

    classifications = []
    if not fm:
        classifications.append('no-frontmatter')
    if not all_tags:
        classifications.append('untagged')
    if not outlinks:
        classifications.append('no-outlinks')
    if word_count < 50 and not fm:
        classifications.append('stub')
    if fm and all_tags and outlinks:
        classifications.append('enriched')
    if fm and (fm['legacy_related'] or fm['has_legacy_created']):
        classifications.append('legacy-schema')
    if fm and fm['legacy_values']:
        classifications.append('legacy-values')

    return {
        'name': name,
        'path': rel_path,
        'folder': top_folder,
        'word_count': word_count,
        'mod_date': mod_date,
        'has_frontmatter': fm is not None,
        'type': fm['type'] if fm else None,
        'maturity': fm['maturity'] if fm and fm['maturity'] in MATURITY_VALUES else None,
        'status': fm['status'] if fm else None,
        'outcome': fm['outcome'] if fm else None,
        'legacy_values': fm['legacy_values'] if fm else [],
        'tags': all_tags,
        'outlinks': outlinks,
        'outlink_count': len(outlinks),
        'classifications': classifications,
    }


def compute_graph(notes):
    """In/out degree, bridge scores, mutual-citation pairs."""
    name_idx = {n['name'].lower(): i for i, n in enumerate(notes)}
    inlink_counts = Counter()
    edges = set()

    for i, n in enumerate(notes):
        for link in n['outlinks']:
            t = link.strip().lower()
            if t in name_idx:
                inlink_counts[t] += 1
                edges.add((i, name_idx[t]))

    mutual_pairs = []
    for (a, b) in edges:
        if a < b and (b, a) in edges:
            mutual_pairs.append((notes[a]['name'], notes[b]['name']))

    neighbor_folders = defaultdict(set)
    for (a, b) in edges:
        neighbor_folders[a].add(notes[b]['folder'])
        neighbor_folders[b].add(notes[a]['folder'])

    for i, n in enumerate(notes):
        key = n['name'].lower()
        n['inlink_count'] = inlink_counts.get(key, 0)
        n['degree'] = n['inlink_count'] + n['outlink_count']
        folders = neighbor_folders.get(i, set()) - {n['folder']}
        n['bridge_score'] = len(folders)
        if n['inlink_count'] == 0 and n['outlink_count'] == 0:
            n['classifications'].append('orphan')

    return mutual_pairs


def find_mocless_clusters(notes, min_size=5):
    """Tags with min_size+ notes and no MOC-typed note carrying that tag."""
    tag_notes = defaultdict(list)
    tag_has_moc = defaultdict(bool)
    for n in notes:
        for t in n['tags']:
            tag_notes[t].append(n['name'])
            if n['type'] == 'moc':
                tag_has_moc[t] = True
    clusters = []
    for tag, members in tag_notes.items():
        if len(members) >= min_size and not tag_has_moc[tag]:
            clusters.append({'tag': tag, 'size': len(members),
                             'sample': members[:6]})
    clusters.sort(key=lambda c: c['size'], reverse=True)
    return clusters


def prioritize(notes):
    for n in notes:
        score = 0
        if 'enriched' in n['classifications'] and 'legacy-values' not in n['classifications']:
            n['priority_score'] = 0
            continue
        if n['folder'] in LOW_PRIORITY_FOLDERS or n['folder'] == '0.Templates':
            n['priority_score'] = 0
            continue
        if n['inlink_count'] > 0 and not n['has_frontmatter']:
            score += 50 + n['inlink_count'] * 10
        if n['folder'] == MAIN_TARGET_FOLDER and n['word_count'] > 200:
            if not n['tags']:
                score += 35
            if n['outlink_count'] == 0:
                score += 20
        if n['folder'] == ACTIVE_FOLDER and not n['has_frontmatter']:
            score += 30
        if not n['has_frontmatter']:
            score += 15
        if not n['tags']:
            score += 10
        if 'legacy-schema' in n['classifications']:
            score += 12
        if 'legacy-values' in n['classifications']:
            score += 12
        mechanical = ('legacy-schema' in n['classifications']
                      or 'legacy-values' in n['classifications'])
        if n['word_count'] < 50 and not mechanical:
            score -= 25  # short note: merge/discard candidate, unless migration
        n['priority_score'] = max(score, 0)


def generate_report(notes, vault_root, mutual_pairs, clusters):
    total = len(notes)
    if total == 0:
        return {'error': 'Empty vault'}
    with_fm = sum(1 for n in notes if n['has_frontmatter'])
    with_tags = sum(1 for n in notes if n['tags'])
    orphans = sum(1 for n in notes if 'orphan' in n['classifications'])
    stubs = sum(1 for n in notes if 'stub' in n['classifications'])
    enriched = sum(1 for n in notes if 'enriched' in n['classifications'])
    legacy_schema = sum(1 for n in notes if 'legacy-schema' in n['classifications'])
    legacy_values = sum(1 for n in notes if 'legacy-values' in n['classifications'])

    tag_counts = Counter(t for n in notes for t in n['tags'])
    by_folder = Counter(n['folder'] for n in notes)
    by_type = Counter(n['type'] for n in notes if n['type'])
    by_maturity = Counter(n['maturity'] for n in notes if n['maturity'])
    by_status = Counter(n['status'] for n in notes if n['status'])

    top_priority = sorted((n for n in notes if n['priority_score'] > 0),
                          key=lambda x: x['priority_score'], reverse=True)[:20]

    leverage = sorted((n for n in notes if n['degree'] > 0),
                      key=lambda x: (x['bridge_score'], x['degree']),
                      reverse=True)[:10]

    return {
        'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'vault_root': str(vault_root),
        'summary': {
            'total_notes': total,
            'with_frontmatter': with_fm,
            'with_frontmatter_pct': round(with_fm / total * 100, 1),
            'with_tags': with_tags,
            'with_tags_pct': round(with_tags / total * 100, 1),
            'orphans': orphans,
            'orphans_pct': round(orphans / total * 100, 1),
            'stubs': stubs,
            'enriched': enriched,
            'enriched_pct': round(enriched / total * 100, 1),
            'legacy_schema': legacy_schema,
            'legacy_values': legacy_values,
        },
        'by_folder': dict(by_folder.most_common()),
        'by_type': dict(by_type.most_common()),
        'by_maturity': dict(by_maturity.most_common()),
        'by_status': dict(by_status.most_common()),
        'top_tags': dict(tag_counts.most_common(30)),
        'graph': {
            'leverage_candidates': [
                {'name': n['name'], 'path': n['path'], 'degree': n['degree'],
                 'inlinks': n['inlink_count'], 'outlinks': n['outlink_count'],
                 'bridge_score': n['bridge_score'], 'folder': n['folder']}
                for n in leverage
            ],
            'mutual_citation_pairs': mutual_pairs[:15],
            'mocless_clusters': clusters[:10],
        },
        'priority_notes': [
            {'name': n['name'], 'path': n['path'], 'score': n['priority_score'],
             'word_count': n['word_count'], 'inlinks': n['inlink_count'],
             'classifications': n['classifications'],
             'legacy_values': n['legacy_values']}
            for n in top_priority
        ],
    }


def scan_vault(vault_root):
    vault_root = Path(vault_root).resolve()
    if not vault_root.exists():
        print(f"Error: {vault_root} does not exist", file=sys.stderr)
        sys.exit(1)
    notes = []
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f.endswith('.md'):
                note = analyze_note(os.path.join(root, f), vault_root)
                if note:
                    notes.append(note)
    mutual_pairs = compute_graph(notes)
    clusters = find_mocless_clusters(notes)
    prioritize(notes)
    return notes, mutual_pairs, clusters


def format_text_report(report):
    if 'error' in report:
        return f"Error: {report['error']}"
    s = report['summary']
    g = report['graph']
    lines = [
        f"# Vault Diagnostic: {report['scan_date']}",
        "",
        f"**Vault:** {report['vault_root']}",
        "",
        "## Summary",
        f"- Total notes: **{s['total_notes']}**",
        f"- With frontmatter: **{s['with_frontmatter']}** ({s['with_frontmatter_pct']}%)",
        f"- With tags: **{s['with_tags']}** ({s['with_tags_pct']}%)",
        f"- Enriched (FM + tags + links): **{s['enriched']}** ({s['enriched_pct']}%)",
        f"- Orphans: **{s['orphans']}** ({s['orphans_pct']}%)",
        f"- Stubs (<50 words, no FM): **{s['stubs']}**",
        f"- Legacy schema (created/related): **{s['legacy_schema']}**",
        f"- Legacy values (PT status/category/origin): **{s['legacy_values']}**",
        "",
        "## By Folder",
    ]
    lines += [f"- {k}: {v}" for k, v in report['by_folder'].items()]
    if report['by_maturity']:
        lines += ["", "## Maturity"] + [f"- {k}: {v}" for k, v in report['by_maturity'].items()]
    if report['by_type']:
        lines += ["", "## Types"] + [f"- {k}: {v}" for k, v in report['by_type'].items()]
    if report['top_tags']:
        lines += ["", "## Top Tags"] + [f"- #{k}: {v}" for k, v in report['top_tags'].items()]

    lines += ["", "## Graph: Leverage Candidates (centrality x cross-domain bridges)"]
    for n in g['leverage_candidates']:
        lines.append(f"- **{n['name']}** ({n['folder']}): degree {n['degree']} "
                     f"(in {n['inlinks']} / out {n['outlinks']}), bridges {n['bridge_score']} domains")
    if g['mutual_citation_pairs']:
        lines += ["", "## Graph: Mutual-Citation Pairs (feedback loops)"]
        lines += [f"- [[{a}]] <-> [[{b}]]" for a, b in g['mutual_citation_pairs']]
    if g['mocless_clusters']:
        lines += ["", "## Graph: MOC-less Clusters (emergent structure candidates)"]
        for c in g['mocless_clusters']:
            lines.append(f"- #{c['tag']}: {c['size']} notes, e.g. {', '.join(c['sample'][:4])}")

    if report['priority_notes']:
        lines += ["", "## Enrichment Priority Queue"]
        for i, n in enumerate(report['priority_notes'], 1):
            cls = ', '.join(n['classifications'])
            lv = f" | migrate: {'; '.join(n['legacy_values'])}" if n['legacy_values'] else ""
            lines.append(f"{i}. **{n['name']}** (score {n['score']}, {n['word_count']} words, "
                         f"{n['inlinks']} inlinks) [{cls}]{lv}")
    return '\n'.join(lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 scan_vault.py "/path/to/vault" [--json] [--output file]')
        sys.exit(1)
    vault_path = sys.argv[1]
    use_json = '--json' in sys.argv
    output_file = None
    if '--output' in sys.argv:
        i = sys.argv.index('--output')
        if i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]

    notes, mutual_pairs, clusters = scan_vault(vault_path)
    report = generate_report(notes, vault_path, mutual_pairs, clusters)
    out = json.dumps(report, ensure_ascii=False, indent=2) if use_json else format_text_report(report)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(out)
        print(f"Report saved to {output_file}")
    else:
        print(out)
