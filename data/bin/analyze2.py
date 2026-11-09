#!/usr/bin/env python3
"""Phase-2 analysis: arms B1-B4 and A2s (tag s3, change C3) against phase-1 controls (tag s2, C3). stdlib only. -> results/analysis-phase2.md"""
import json, glob, os, random, statistics as st
from math import comb
from collections import defaultdict
R = os.path.expanduser('~/study-mfe/s2/results')
runs = []
for f in sorted(glob.glob(f'{R}/s[23]-C3-*/summary.json')):
    s = json.load(open(f))
    if s.get('agent_error') is True or not (s.get('agent_tokens') or 0): continue
    s['hidden_cloned'] = (s.get('hidden') or 'reports') in (s.get('repos_cloned') or [])
    s['any_miss'] = int(bool(s.get('missed')))
    runs.append(s)
DESC = {'A1': 'open / none (phase 1)', 'A2': 'structured / partial (phase 1)', 'A3': 'structured / complete (phase 1)', 'A5': 'open / catalog (phase 1)',
        'B1': 'partial + "find every app" instruction', 'B2': 'partial + global audit check', 'B3': 'partial + st ask available', 'B4': 'partial + "others may be affected"', 'A2s': 'partial, hidden = core-shell'}
def fisher(a, b, c, d):
    n1, n2, k = a + b, c + d, a + c; N = n1 + n2
    pr = lambda x: comb(n1, x) * comb(n2, k - x) / comb(N, k)
    p0 = pr(a); return min(1.0, sum(pr(x) for x in range(max(0, k - n2), min(n1, k) + 1) if pr(x) <= p0 + 1e-12))
def mean(x): x = [v for v in x if v is not None]; return sum(x) / len(x) if x else float('nan')
def med(x): x = [v for v in x if v is not None]; return st.median(x) if x else float('nan')
def boot(a, b, n=4000):
    a = [v for v in a if v is not None]; b = [v for v in b if v is not None]
    if len(a) < 2 or len(b) < 2: return (float('nan'), float('nan'))
    r = random.Random(3); d = sorted(mean([r.choice(a) for _ in a]) - mean([r.choice(b) for _ in b]) for _ in range(n)); return d[int(.025 * n)], d[int(.975 * n)]
g = defaultdict(list)
for r in runs: g[(r['arm'], r['topology'])].append(r)
out = []; P = out.append
P('# Phase 2 analysis (change C3, Sonnet)\n')
P(f"Valid runs: {len(runs)}. New arms (s3): {sum(1 for r in runs if r['tag']=='s3')}; phase-1 controls (s2, C3): {sum(1 for r in runs if r['tag']=='s2')}.\n")
P('## Misses and behaviour\n')
P('| arm | layout | n | runs with a miss | cloned the hidden repo | ran `st audit` (runs / last report clean) | used `st ask` | tasks recorded (mean) | vs A2: Fisher p | vs A1: Fisher p |')
P('|---|---|---|---|---|---|---|---|---|---|')
for arm in ('A1', 'A2', 'A3', 'A5', 'B1', 'B2', 'B3', 'B4', 'A2s'):
    for lay in ('multi', 'mono'):
        rs = g.get((arm, lay), [])
        if not rs: continue
        m = sum(r['any_miss'] for r in rs); n = len(rs)
        def p(ref):
            q = g.get((ref, lay), [])
            if not q or ref == arm: return '-'
            return f"{fisher(m, n-m, sum(x['any_miss'] for x in q), len(q)-sum(x['any_miss'] for x in q)):.3f}"
        aud = [r for r in rs if r.get('audit_runs')]
        P(f"| {arm} {DESC[arm]} | {lay} | {n} | {m}/{n} | {sum(r['hidden_cloned'] for r in rs)}/{n} | {len(aud)}/{n} ({sum(1 for r in aud if r.get('audit_last_violations')==0)} clean) | {sum(1 for r in rs if r.get('asks'))}/{n} | {mean([r.get('subtasks_recorded') for r in rs]):.1f} | {p('A2')} | {p('A1')} |")
P('\n## Cost among correct runs only (multi-repo)\n')
P('| arm | n correct | PRs | turnaround s (median) | tokens k (mean) | turnaround diff vs A2-correct-or-A1 [95% CI] |')
P('|---|---|---|---|---|---|')
base = [r for r in g.get(('A1', 'multi'), []) if r['acceptance_pass']]
for arm in ('A1', 'A3', 'A5', 'B1', 'B2', 'B3', 'B4', 'A2s'):
    rs = [r for r in g.get((arm, 'multi'), []) if r['acceptance_pass']]
    if not rs: P(f'| {arm} | 0 | | | | |'); continue
    lo, hi = boot([r['turnaround_s'] for r in rs], [r['turnaround_s'] for r in base]) if arm != 'A1' else (float('nan'),) * 2
    P(f"| {arm} {DESC[arm]} | {len(rs)} | {mean([r['prs'] for r in rs]):.1f} | {med([r['turnaround_s'] for r in rs]):.0f} | {mean([r['agent_tokens'] for r in rs])/1000:.0f} | [{lo:.0f}, {hi:.0f}] (vs A1) |")
txt = '\n'.join(out); open(f'{R}/analysis-phase2.md', 'w').write(txt); print(txt)
