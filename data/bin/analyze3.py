#!/usr/bin/env python3
"""Phase-3 analysis: C3 arms at 17 repositories (tag s4) against the same arm at 5 repositories (tag s2, or s3 for B4). stdlib only."""
import json, glob, os, random, statistics as st
from math import comb
from collections import defaultdict
R = os.path.expanduser('~/study-mfe/s2/results')
runs = []
for f in sorted(glob.glob(f'{R}/s[234]-C3-*/summary.json')):
    s = json.load(open(f))
    if s.get('agent_error') is True or not (s.get('agent_tokens') or 0): continue
    s['estate'] = 17 if s['tag'] == 's4' else 5
    s['any_miss'] = int(bool(s.get('missed'))); s['n_cloned'] = len(s.get('repos_cloned') or [])
    s['hidden_cloned'] = 'reports' in (s.get('repos_cloned') or [])
    runs.append(s)
def fisher(a, b, c, d):
    n1, n2, k = a + b, c + d, a + c; N = n1 + n2
    pr = lambda x: comb(n1, x) * comb(n2, k - x) / comb(N, k)
    p0 = pr(a); return min(1.0, sum(pr(x) for x in range(max(0, k - n2), min(n1, k) + 1) if pr(x) <= p0 + 1e-12))
def mean(x): x = [v for v in x if v is not None]; return sum(x) / len(x) if x else float('nan')
def med(x): x = [v for v in x if v is not None]; return st.median(x) if x else float('nan')
def boot(a, b, n=4000):
    a = [v for v in a if v is not None]; b = [v for v in b if v is not None]
    if len(a) < 2 or len(b) < 2: return (float('nan'),) * 2
    r = random.Random(5); d = sorted(mean([r.choice(a) for _ in a]) - mean([r.choice(b) for _ in b]) for _ in range(n)); return d[int(.025 * n)], d[int(.975 * n)]
g = defaultdict(list)
for r in runs: g[(r['arm'], r['topology'], r['estate'])].append(r)
DESC = {'A1': 'open / none', 'A2': 'structured / partial', 'A3': 'structured / complete', 'A5': 'open / catalog complete', 'A6': 'open / catalog stale', 'B4': 'partial + "others may be affected"'}
out = []; P = out.append
P('# Phase 3 analysis: 17 repositories against 5 (change C3, Sonnet)\n')
P(f"Valid runs: {sum(1 for r in runs if r['estate']==17)} at 17 repositories; controls at 5 repositories: {sum(1 for r in runs if r['estate']==5)} (phase 1/2, not concurrent).\n")
P('## Misses and exploration\n')
P('| arm | layout | repos | n | runs with a miss | mean repos cloned | cloned the hidden repo | Fisher p (17 vs 5) |')
P('|---|---|---|---|---|---|---|---|')
for arm in DESC:
    for lay in ('multi', 'mono'):
        for e in (5, 17):
            rs = g.get((arm, lay, e), [])
            if not rs: continue
            m = sum(r['any_miss'] for r in rs); n = len(rs)
            p = '-'
            if e == 17 and g.get((arm, lay, 5)):
                q = g[(arm, lay, 5)]; mq = sum(r['any_miss'] for r in q); p = f'{fisher(m, n-m, mq, len(q)-mq):.3f}'
            P(f"| {arm} {DESC[arm]} | {lay} | {e} | {n} | {m}/{n} | {mean([r['n_cloned'] for r in rs]):.1f} | {sum(r['hidden_cloned'] for r in rs)}/{n} | {p} |")
P('\n## Cost of the larger estate (all runs, 17 vs 5)\n')
P('| arm | layout | tokens k: 5 -> 17 | turnaround s median: 5 -> 17 | turnaround diff [95% CI] | PRs 5 -> 17 |')
P('|---|---|---|---|---|---|')
for arm in DESC:
    for lay in ('multi', 'mono'):
        a, b = g.get((arm, lay, 5), []), g.get((arm, lay, 17), [])
        if not a or not b: continue
        lo, hi = boot([r['turnaround_s'] for r in b], [r['turnaround_s'] for r in a])
        P(f"| {arm} {DESC[arm]} | {lay} | {mean([r['agent_tokens'] for r in a])/1000:.0f} -> {mean([r['agent_tokens'] for r in b])/1000:.0f} | {med([r['turnaround_s'] for r in a]):.0f} -> {med([r['turnaround_s'] for r in b]):.0f} | [{lo:.0f}, {hi:.0f}] | {mean([r['prs'] for r in a]):.1f} -> {mean([r['prs'] for r in b]):.1f} |")
txt = '\n'.join(out); open(f'{R}/analysis-phase3.md', 'w').write(txt); print(txt)
