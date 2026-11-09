#!/usr/bin/env python3
"""Phase 6 analysis: two developers on one ticket, handoff conditions H0/H1/H2 (tag s6). stdlib only. -> results/analysis-phase6.md"""
import json, glob, os, sys, statistics as st
TAG = sys.argv[1] if len(sys.argv) > 1 else "s6"; OUTN = sys.argv[2] if len(sys.argv) > 2 else "analysis-phase6.md"
from math import comb
from collections import defaultdict
R = os.path.expanduser('~/study-mfe/s2/results')
runs = []
for f in sorted(glob.glob(f'{R}/{TAG}-T-*/summary.json')):
    s = json.load(open(f))
    if not s.get('agents_ok'): continue
    runs.append(s)
def fisher(a, b, c, d):
    n1, n2, k = a + b, c + d, a + c; N = n1 + n2
    pr = lambda x: comb(n1, x) * comb(n2, k - x) / comb(N, k); p0 = pr(a)
    return min(1.0, sum(pr(x) for x in range(max(0, k - n2), min(n1, k) + 1) if pr(x) <= p0 + 1e-12))
mean = lambda x: sum(x) / len(x) if x else float('nan')
med = lambda x: st.median(x) if x else float('nan')
g = defaultdict(list)
for r in runs: g[(r['arm'], r['topology'])].append(r)
D = {'H0': 'no channel', 'H1': 'free messages', 'H2': 'required handoff note'}
o = []; P = o.append
P('# Phase 6: two developers, one ticket (change C3, complete list, Sonnet)\n')
P(f'Valid runs: {len(runs)} (agents ran without an API error; a developer who never signalled done is counted as a timeout).\n')
P('| condition | layout | n | complete | merge conflicts (mean) | PRs (mean) | PR updates | CI failures | makespan s (median) | timeouts | free messages | handoff notes posted / read | dev-b waiting on the other dev, s (mean) | tokens k (mean) | cost $ |')
P('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for lay in ('multi', 'mono'):
    for arm in ('H0', 'H1', 'H2'):
        rs = g.get((arm, lay), [])
        if not rs: continue
        P(f"| {arm} {D[arm]} | {lay} | {len(rs)} | {sum(r['acceptance_pass'] for r in rs)}/{len(rs)} | {mean([r['merge_conflicts'] for r in rs]):.1f} | {mean([r['prs'] for r in rs]):.1f} | {mean([r['pr_updates'] for r in rs]):.1f} | {sum(r['ci_failures'] for r in rs)} | {med([r['makespan_s'] for r in rs]):.0f} | {sum(len(r.get('timeouts') or []) for r in rs)} | {mean([r['msgs_total'] for r in rs]):.1f} | {sum(r['handoffs_posted'] for r in rs)} / {sum(r['handoff_reads'] for r in rs)} | {mean([r['dev_b_comm_wait_s'] for r in rs]):.0f} | {mean([r['agent_tokens'] for r in rs])/1000:.0f} | {mean([r['agent_cost_usd'] for r in rs]):.2f} |")
P('\n## Release class chosen by dev-a, and slow adoption by dev-b (multi-repo)\n')
P('| condition | classes chosen (major / minor / patch / none) | dev-b finished after 300 s | dev-b finish s (sorted) | dev-b merge after contract live, s (sorted) |')
P('|---|---|---|---|---|')
for arm in ('H0', 'H1', 'H2'):
    rs = g.get((arm, 'multi'), [])
    if not rs: continue
    cl = [r.get('semver_class') for r in rs]
    P(f"| {arm} {D[arm]} | {cl.count('major')} / {cl.count('minor')} / {cl.count('patch')} / {cl.count(None)+cl.count('none')} | {sum(1 for r in rs if (r.get('dev_b_finished_s') or 0) > 300)}/{len(rs)} | {sorted(r.get('dev_b_finished_s') for r in rs)} | {sorted(r.get('handoff_to_dependent_merge_s') for r in rs if r.get('handoff_to_dependent_merge_s') is not None)} |")
P('\n## Completeness: pairwise (Fisher exact, multi-repo)\n')
P('| comparison | complete / n (first) | complete / n (second) | p |')
P('|---|---|---|---|')
for a1, a2 in (('H0', 'H1'), ('H0', 'H2'), ('H1', 'H2')):
    x, y = g.get((a1, 'multi'), []), g.get((a2, 'multi'), [])
    if x and y:
        kx, ky = sum(r['acceptance_pass'] for r in x), sum(r['acceptance_pass'] for r in y)
        P(f'| {a1} vs {a2} | {kx}/{len(x)} | {ky}/{len(y)} | {fisher(kx, len(x)-kx, ky, len(y)-ky):.3f} |')
P('\n## Incomplete or odd runs\n')
for r in runs:
    odd = []
    if not r['acceptance_pass']: odd.append('missed=' + ','.join(r.get('missed') or []))
    if r.get('timeouts'): odd.append('timeout=' + ','.join(r['timeouts']))
    if r['merge_conflicts']: odd.append(f"merge_conflicts={r['merge_conflicts']}")
    if r['ci_failures']: odd.append(f"ci_failures={r['ci_failures']}")
    if r['arm'] == 'H2' and r['handoffs_posted'] == 0: odd.append('no handoff posted')
    if odd: P(f"* {r['run']}: " + '; '.join(odd))
txt = '\n'.join(o); open(f'{R}/{OUTN}', 'w').write(txt); print(txt)
