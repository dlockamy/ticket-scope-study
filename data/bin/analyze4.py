#!/usr/bin/env python3
"""Phase-4: smaller model (tag s5) on C3, 5 arms; compared with Sonnet on the same arms (s2/s3 controls, C3)."""
import json, glob, os
from math import comb
from collections import defaultdict
R = os.path.expanduser('~/study-mfe/s2/results')
def load(pat, model):
    out = []
    for f in sorted(glob.glob(f'{R}/{pat}/summary.json')):
        s = json.load(open(f))
        if s.get('agent_error') is True or not (s.get('agent_tokens') or 0): continue
        s['m'] = model; s['any_miss'] = int(bool(s.get('missed'))); s['n_cloned'] = len(s.get('repos_cloned') or []); s['hid'] = 'reports' in (s.get('repos_cloned') or []); out.append(s)
    return out
H = load('s5-C3-*', 'haiku')
S = [r for r in load('s2-C3-*', 'sonnet') + load('s3-C3-*', 'sonnet')]
def fisher(a, b, c, d):
    n1, n2, k = a + b, c + d, a + c; N = n1 + n2
    pr = lambda x: comb(n1, x) * comb(n2, k - x) / comb(N, k); p0 = pr(a)
    return min(1.0, sum(pr(x) for x in range(max(0, k - n2), min(n1, k) + 1) if pr(x) <= p0 + 1e-12))
mean = lambda x: sum(x) / len(x) if x else float('nan')
g = defaultdict(list)
for r in H + S: g[(r['m'], r['arm'], r['topology'])].append(r)
D = {'A1': 'open / none', 'A2': 'structured / partial', 'B1': '"find every app"', 'B2': 'global audit', 'B4': '"others may be affected"'}
o = []; P = o.append
P('# Phase 4: smaller model against Sonnet (change C3, 5 repositories)\n')
P(f'Valid runs: smaller model {len(H)}; Sonnet controls used {sum(1 for r in S if r["arm"] in D)}.\n')
P('| arm | layout | smaller model: misses / n | Fisher p vs its A2 | opened hidden repo | ran audit | tokens k (mean) | Sonnet: misses / n | Sonnet tokens k | token ratio |')
P('|---|---|---|---|---|---|---|---|---|---|')
for arm in D:
    for lay in ('multi', 'mono'):
        h = g.get(('haiku', arm, lay), []); s = g.get(('sonnet', arm, lay), [])
        if not h: continue
        m = sum(r['any_miss'] for r in h); n = len(h)
        base = g.get(('haiku', 'A2', lay), []); mb = sum(r['any_miss'] for r in base)
        p = '-' if arm == 'A2' or not base else f'{fisher(m, n-m, mb, len(base)-mb):.3f}'
        ms = sum(r['any_miss'] for r in s)
        th = mean([r['agent_tokens'] for r in h]) / 1000; ts = mean([r['agent_tokens'] for r in s]) / 1000
        P(f"| {arm} {D[arm]} | {lay} | {m}/{n} | {p} | {sum(r['hid'] for r in h)}/{n} | {sum(1 for r in h if r.get('audit_runs'))}/{n} | {th:.0f} | {ms}/{len(s)} | {ts:.0f} | {th/ts:.1f}x |")
txt = '\n'.join(o); open(f'{R}/analysis-phase4.md', 'w').write(txt); print(txt)
