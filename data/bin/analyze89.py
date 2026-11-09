#!/usr/bin/env python3
"""Phases 8 (epics, tag s8) and 9 (noisy tickets, tag s9), change C3, against phase-1 controls (tag s2). stdlib only."""
import json, glob, os, random, statistics as st
from math import comb
from collections import defaultdict
R = os.path.expanduser('~/study-mfe/s2/results')
runs = []
for pat in ('s2-C3-*', 's8-C3-*', 's9-C3-*'):
    for f in sorted(glob.glob(f'{R}/{pat}/summary.json')):
        s = json.load(open(f))
        if s.get('agent_error') is True or not (s.get('agent_tokens') or 0): continue
        s['any_miss'] = int(bool(s.get('missed'))); s['n_cloned'] = len(s.get('repos_cloned') or []); s['hid'] = 'reports' in (s.get('repos_cloned') or [])
        ev = [json.loads(l) for l in open(f.replace('summary.json', 'events.jsonl'))]
        s['refused'] = sum(1 for e in ev if e['event'] == 'done_refused'); s['child_done'] = sum(1 for e in ev if e['event'] == 'child_done')
        s['children_opened'] = len({e.get('child') for e in ev if e['event'] == 'child_opened'}); s['children_closed'] = len({e.get('child') for e in ev if e['event'] == 'child_done'})
        TEAM = {'shell': 'platform', 'billing': 'payments', 'reports': 'insights'}
        unf = wrong = 0
        for k, v in (s.get('consumers') or {}).items():
            if v.get('src_ok') and v.get('live_ok'): continue
            lo = v.get('live_owner')
            if lo and lo != TEAM[k]: wrong += 1
            else: unf += 1
        s['n_unfixed'] = unf; s['n_wrong_value'] = wrong
        runs.append(s)
def fisher(a, b, c, d):
    n1, n2, k = a + b, c + d, a + c; N = n1 + n2
    pr = lambda x: comb(n1, x) * comb(n2, k - x) / comb(N, k); p0 = pr(a)
    return min(1.0, sum(pr(x) for x in range(max(0, k - n2), min(n1, k) + 1) if pr(x) <= p0 + 1e-12))
mean = lambda x: sum(x) / len(x) if x else float('nan'); med = lambda x: st.median(x) if x else float('nan')
def boot(a, b, n=4000):
    if len(a) < 2 or len(b) < 2: return (float('nan'),) * 2
    r = random.Random(11); d = sorted(mean([r.choice(a) for _ in a]) - mean([r.choice(b) for _ in b]) for _ in range(n)); return d[int(.025 * n)], d[int(.975 * n)]
g = defaultdict(list)
for r in runs: g[(r['arm'], r['topology'])].append(r)
D = {'A1': 'clean open-ended (control)', 'A2': 'single ticket, partial list (control)', 'A3': 'single ticket, complete list (control)',
     'E1': 'epic, children without reports', 'E2': 'epic, children incl. reports', 'E3': 'epic, partial + final "verify" child',
     'N1': 'terse', 'N2': 'rambling thread', 'N3': 'stale library name'}
o = []; P = o.append
P('# Phases 8 and 9 (change C3, Sonnet): epics and noisy tickets\n')
P(f"Valid runs: phase 8 {sum(1 for r in runs if r['tag']=='s8')}, phase 9 {sum(1 for r in runs if r['tag']=='s9')}, phase-1 controls used {sum(1 for r in runs if r['tag']=='s2' and r['arm'] in ('A1','A2','A3'))}.\n")
P('| arm | layout | n | complete (all three apps live, right values) | runs with an app left unfixed | runs with a wrong owner value | opened the hidden repo | repos cloned | PRs | turnaround s (median) | tokens k (mean) | cost $ | child tickets opened / closed | epic closes refused |')
P('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for arm in D:
    for lay in ('multi', 'mono'):
        rs = g.get((arm, lay), [])
        if not rs: continue
        P(f"| {arm} {D[arm]} | {lay} | {len(rs)} | {sum(r['acceptance_pass'] for r in rs)}/{len(rs)} | {sum(1 for r in rs if r['n_unfixed'])}/{len(rs)} | {sum(1 for r in rs if r['n_wrong_value'])}/{len(rs)} | {sum(r['hid'] for r in rs)}/{len(rs)} | {mean([r['n_cloned'] for r in rs]):.1f} | {mean([r['prs'] for r in rs]):.1f} | {med([r['turnaround_s'] for r in rs]):.0f} | {mean([r['agent_tokens'] for r in rs])/1000:.0f} | {mean([r['agent_cost_usd'] for r in rs]):.2f} | {mean([r['children_opened'] for r in rs]):.1f} / {mean([r['children_closed'] for r in rs]):.1f} | {sum(r['refused'] for r in rs)} |")
P('\n## Misses against the control, multi-repo (Fisher exact)\n')
P('| arm | misses / n | control | control misses / n | p |')
P('|---|---|---|---|---|')
ctrl = {'E1': 'A2', 'E2': 'A3', 'E3': 'A2', 'N1': 'A1', 'N2': 'A1', 'N3': 'A1'}
for arm, c in ctrl.items():
    a, b = g.get((arm, 'multi'), []), g.get((c, 'multi'), [])
    if a and b:
        ka, kb = sum(r['any_miss'] for r in a), sum(r['any_miss'] for r in b)
        P(f'| {arm} {D[arm]} | {ka}/{len(a)} | {c} | {kb}/{len(b)} | {fisher(ka, len(a)-ka, kb, len(b)-kb):.3f} |')
P('\n## Cost against the control (multi-repo, all runs)\n')
P('| arm | control | tokens k: control -> arm | turnaround s median: control -> arm | turnaround diff [95% CI] |')
P('|---|---|---|---|---|')
for arm, c in ctrl.items():
    a, b = g.get((arm, 'multi'), []), g.get((c, 'multi'), [])
    if a and b:
        lo, hi = boot([r['turnaround_s'] for r in a], [r['turnaround_s'] for r in b])
        P(f"| {arm} | {c} | {mean([r['agent_tokens'] for r in b])/1000:.0f} -> {mean([r['agent_tokens'] for r in a])/1000:.0f} | {med([r['turnaround_s'] for r in b]):.0f} -> {med([r['turnaround_s'] for r in a]):.0f} | [{lo:.0f}, {hi:.0f}] |")
txt = '\n'.join(o); open(f'{R}/analysis-phase89.md', 'w').write(txt); print(txt)
