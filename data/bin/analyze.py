#!/usr/bin/env python3
"""Analysis for the ticket-structure/process study (stdlib only). usage: analyze.py [tag-prefix]  -> prints markdown, writes results/analysis.md

Valid run = agent ran without API/auth error, produced tokens, and a summary exists. Everything else is excluded and counted.
Decision rules follow monorepo-followup-ticket-process-prereg:
  * practice 'helps' on an outcome only if it lowers it >= 20% vs the open-ended no-information baseline (A1) in the same layout and change type,
    the bootstrap 95% interval for the difference excludes zero, and (if a second-model subset exists) it points the same way there.
  * variance decomposition per outcome: share of variance by layout, arm, change type (sequential sums of squares, order layout->change->arm->layout x arm).
"""
import json, glob, os, random, sys, statistics as st
from collections import defaultdict

R = os.path.expanduser('~/study-mfe/s2/results')
prefix = sys.argv[1] if len(sys.argv) > 1 else 's2-'
OUTC = ['n_missed', 'any_miss', 'hidden_miss', 'prs', 'jenkins_builds', 'turnaround_s', 'rework_events', 'repeat_repo_prs', 'n_cloned', 'agent_tokens', 'agent_cost_usd']
ARM_DESC = {'A1': 'open / none', 'A2': 'structured / partial', 'A3': 'structured / complete', 'A4': 'structured / decoy', 'A5': 'open / catalog complete', 'A6': 'open / catalog stale', 'A7': 'structured+checks / partial'}

runs, excluded = [], []
for f in sorted(glob.glob(f'{R}/{prefix}*/summary.json')):
    s = json.load(open(f)); name = os.path.basename(os.path.dirname(f))
    ok = s.get('agent_error') is not True and (s.get('agent_tokens') or 0) > 0 and s.get('finished') in ('done', 'blocked')
    sk = {}
    try: sk = json.load(open(os.path.dirname(f) + '/skew.json'))
    except Exception: pass
    if not ok: excluded.append((name, s.get('finished'), s.get('agent_error'))); continue
    missed = s.get('missed') or []
    r = dict(name=name, layout=s['topology'], change=s['change'], arm=s['arm'], rep=s['rep'], model=s['model'], tag=s['tag'],
             passed=bool(s.get('acceptance_pass')), finished=s['finished'], n_missed=len(missed), any_miss=int(len(missed) > 0),
             hidden_miss=int('reports' in missed), prs=s.get('prs'), jenkins_builds=s.get('jenkins_builds'), turnaround_s=s.get('turnaround_s'),
             rework_events=s.get('rework_events'), repeat_repo_prs=s.get('repeat_repo_prs'), n_cloned=len(s.get('repos_cloned') or []),
             agent_tokens=s.get('agent_tokens'), agent_cost_usd=s.get('agent_cost_usd'), decoy_touched=int(bool(s.get('decoy_touched'))),
             deps_queries=s.get('deps_queries', 0), semver_ok=s.get('semver_ok'), skew=max(abs(sk.get('skew_start_s', 0)), abs(sk.get('skew_end_s', 0))))
    runs.append(r)

def mean(x): x = [v for v in x if v is not None]; return sum(x) / len(x) if x else float('nan')
def med(x): x = [v for v in x if v is not None]; return st.median(x) if x else float('nan')
def boot_diff(a, b, n=4000, seed=1):
    """bootstrap 95% CI of mean(a)-mean(b)"""
    a = [v for v in a if v is not None]; b = [v for v in b if v is not None]
    if len(a) < 2 or len(b) < 2: return (float('nan'), float('nan'))
    rng = random.Random(seed); d = []
    for _ in range(n): d.append(mean([rng.choice(a) for _ in a]) - mean([rng.choice(b) for _ in b]))
    d.sort(); return d[int(.025 * n)], d[int(.975 * n)]
def f(x, p=1): return 'n/a' if x != x else f'{x:.{p}f}'

main = [r for r in runs if r['tag'] == 's2']
second = [r for r in runs if r['tag'] == 's2h']
out = []
P = out.append
P(f'# Analysis ({prefix}*)\n')
P(f'Valid runs: **{len(runs)}** (main model {len(main)}, second model {len(second)}). Excluded (agent/auth error or unfinished): {len(excluded)}.')
big_skew = [r['name'] for r in runs if r['skew'] > 30]
if big_skew: P(f'Runs with VM clock skew > 30 s at start or end of the round (timing suspect): {len(big_skew)}.')
reps = defaultdict(int)
for r in main: reps[(r['change'], r['arm'], r['layout'])] += 1
if reps: P(f'Replicates per cell (main model): min {min(reps.values())}, max {max(reps.values())}, cells {len(reps)}.\n')

# ---- per-cell table
P('## Per-cell results (main model)\n')
P('| change | arm | layout | n | pass | any miss | hidden (reports) missed | PRs | builds | turnaround s (median) | rework | repeat-repo PRs | clones | tokens (k) | cost $ | decoy touched |')
P('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
cells = defaultdict(list)
for r in main: cells[(r['change'], r['arm'], r['layout'])].append(r)
for k in sorted(cells):
    g = cells[k]
    P(f"| {k[0]} | {k[1]} {ARM_DESC[k[1]]} | {k[2]} | {len(g)} | {sum(x['passed'] for x in g)}/{len(g)} | {sum(x['any_miss'] for x in g)}/{len(g)} | {sum(x['hidden_miss'] for x in g)}/{len(g)} | {f(mean([x['prs'] for x in g]))} | {f(mean([x['jenkins_builds'] for x in g]))} | {f(med([x['turnaround_s'] for x in g]),0)} | {f(mean([x['rework_events'] for x in g]),2)} | {f(mean([x['repeat_repo_prs'] for x in g]),2)} | {f(mean([x['n_cloned'] for x in g]))} | {f(mean([x['agent_tokens'] for x in g])/1000,0)} | {f(mean([x['agent_cost_usd'] for x in g]),2)} | {sum(x['decoy_touched'] for x in g)} |")

# ---- layout effect by change type
P('\n## Layout effect by change type (all arms pooled, main model)\n')
P('| change | outcome | monorepo mean | multi-repo mean | diff (multi - mono) [95% boot CI] |')
P('|---|---|---|---|---|')
for ch in ('C1', 'C2', 'C3'):
    for o in ('any_miss', 'prs', 'jenkins_builds', 'turnaround_s', 'rework_events', 'n_cloned', 'agent_tokens'):
        a = [r[o] for r in main if r['change'] == ch and r['layout'] == 'multi']; b = [r[o] for r in main if r['change'] == ch and r['layout'] == 'mono']
        if not a or not b: continue
        lo, hi = boot_diff(a, b)
        P(f'| {ch} | {o} | {f(mean(b),2)} | {f(mean(a),2)} | {f(mean(a)-mean(b),2)} [{f(lo,2)}, {f(hi,2)}] |')

# ---- practice effect vs A1 baseline (the 20% rule)
P('\n## Practice vs the open-ended baseline A1 (within layout and change type)\n')
P('Lower is better for every outcome shown. "Rule" = at least 20% lower AND the 95% interval of the difference excludes zero. HARM = at least 20% higher AND the interval excludes zero.\n')
P('| change | layout | arm | outcome | A1 mean | arm mean | change % | 95% CI of diff | n (A1/arm) | verdict |')
P('|---|---|---|---|---|---|---|---|---|---|')
for ch in ('C2', 'C3'):
    for lay in ('mono', 'multi'):
        base = cells.get((ch, 'A1', lay), [])
        for arm in ('A2', 'A3', 'A4', 'A5', 'A6', 'A7'):
            g = cells.get((ch, arm, lay), [])
            if not base or not g: continue
            for o in ('any_miss', 'rework_events', 'turnaround_s', 'prs', 'agent_tokens'):
                a = [x[o] for x in g]; b = [x[o] for x in base]
                mb, ma = mean(b), mean(a)
                pct = (ma - mb) / mb * 100 if mb else float('nan')
                lo, hi = boot_diff(a, b)
                verdict = ''
                if mb and pct <= -20 and hi < 0: verdict = 'RULE MET'
                elif mb and pct >= 20 and lo > 0: verdict = 'HARM'
                elif mb and abs(pct) >= 20: verdict = 'large but interval spans 0'
                P(f'| {ch} | {lay} | {arm} {ARM_DESC[arm]} | {o} | {f(mb,2)} | {f(ma,2)} | {f(pct,0) if pct==pct else "n/a"} | [{f(lo,2)}, {f(hi,2)}] | {len(base)}/{len(g)} | {verdict} |')

# ---- variance decomposition
def decompose(rows, o):
    ys = [r[o] for r in rows if r[o] is not None]
    rows = [r for r in rows if r[o] is not None]
    if len(rows) < 8: return None
    mu = mean(ys); sst = sum((y - mu) ** 2 for y in ys)
    if sst == 0: return None
    def ss_of(keyf, resid):
        g = defaultdict(list)
        for r, e in zip(rows, resid): g[keyf(r)].append(e)
        fitted = {k: mean(v) for k, v in g.items()}
        return sum(len(v) * fitted[k] ** 2 for k, v in g.items()), [e - fitted[keyf(r)] for r, e in zip(rows, resid)]
    resid = [y - mu for y in ys]; res = {}
    for name, kf in (('layout', lambda r: r['layout']), ('change type', lambda r: r['change']), ('arm', lambda r: r['arm']), ('layout x arm', lambda r: (r['layout'], r['arm'])), ('layout x change', lambda r: (r['layout'], r['change']))):
        ss, resid = ss_of(kf, resid); res[name] = ss / sst
    res['replicate noise (residual)'] = sum(e * e for e in resid) / sst
    return res
P('\n## Share of variance explained (sequential sums of squares, main model, C2+C3 only for miss outcomes)\n')
P('Order of entry: layout, change type, arm, layout x arm, layout x change. Order matters when factors are unbalanced; with an incomplete matrix read these as rough shares, not tests.\n')
P('| outcome | layout | change type | arm (process levers) | layout x arm | layout x change | residual |')
P('|---|---|---|---|---|---|---|')
for o in ('any_miss', 'n_missed', 'prs', 'jenkins_builds', 'turnaround_s', 'rework_events', 'n_cloned', 'agent_tokens'):
    rows = [r for r in main if r['change'] in ('C2', 'C3')] if o in ('any_miss', 'n_missed') else main
    d = decompose(rows, o)
    if d: P(f"| {o} | {d['layout']*100:.0f}% | {d['change type']*100:.0f}% | {d['arm']*100:.0f}% | {d['layout x arm']*100:.0f}% | {d['layout x change']*100:.0f}% | {d['replicate noise (residual)']*100:.0f}% |")

# ---- misses by layout and arm, per change
P('\n## Misses (a consumer not updated and live) by layout and arm\n')
P('| change | arm | mono: runs with a miss | multi: runs with a miss | mono hidden missed | multi hidden missed |')
P('|---|---|---|---|---|---|')
for ch in ('C2', 'C3'):
    for arm in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'):
        a, b = cells.get((ch, arm, 'mono'), []), cells.get((ch, arm, 'multi'), [])
        if a or b: P(f"| {ch} | {arm} | {sum(x['any_miss'] for x in a)}/{len(a)} | {sum(x['any_miss'] for x in b)}/{len(b)} | {sum(x['hidden_miss'] for x in a)}/{len(a)} | {sum(x['hidden_miss'] for x in b)}/{len(b)} |")

# ---- second model
if second:
    P('\n## Second model subset\n')
    P('| change | arm | layout | n | pass | any miss | PRs | turnaround s (median) | tokens (k) |')
    P('|---|---|---|---|---|---|---|---|---|')
    c2 = defaultdict(list)
    for r in second: c2[(r['change'], r['arm'], r['layout'])].append(r)
    for k in sorted(c2):
        g = c2[k]; P(f"| {k[0]} | {k[1]} | {k[2]} | {len(g)} | {sum(x['passed'] for x in g)}/{len(g)} | {sum(x['any_miss'] for x in g)}/{len(g)} | {f(mean([x['prs'] for x in g]))} | {f(med([x['turnaround_s'] for x in g]),0)} | {f(mean([x['agent_tokens'] for x in g])/1000,0)} |")

# ---- exact tests for misses (baseline is often 0, so the percentage rule cannot see them)
from math import comb
def fisher(a, b, c, d):
    """two-sided Fisher exact p for [[a,b],[c,d]] (a,b = successes,failures in group 1; c,d in group 2)"""
    n1, n2, k = a + b, c + d, a + c; N = n1 + n2
    def pr(x): return comb(n1, x) * comb(n2, k - x) / comb(N, k)
    p0 = pr(a); lo, hi = max(0, k - n2), min(n1, k)
    return min(1.0, sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0 + 1e-12))
P('\n## Misses: each arm against the references (multi-repo; the monorepo had no misses to test)\n')
P('Fisher exact, two-sided, on runs with any miss. Reference 1 = A1 (open-ended, no information). Reference 2 = A3 (structured, complete list).\n')
P('| change | arm | misses / n | vs A1: p | vs A3: p | reading |')
P('|---|---|---|---|---|---|')
for ch in ('C2', 'C3', 'C2+C3'):
    def grp(arm): 
        g = [x for x in main if x['layout'] == 'multi' and x['arm'] == arm and (x['change'] in ch.split('+'))]
        return sum(x['any_miss'] for x in g), len(g)
    m1, n1 = grp('A1'); m3, n3 = grp('A3')
    for arm in ('A2', 'A3', 'A4', 'A5', 'A6', 'A7'):
        m, n = grp(arm)
        if not n: continue
        p1 = fisher(m, n - m, m1, n1 - m1); p3 = fisher(m, n - m, m3, n3 - m3)
        rd = 'more misses than A1' if (p1 < .05 and m > m1) else ('fewer misses than A1' if (p1 < .05 and m < m1) else 'no clear difference from A1')
        P(f'| {ch} | {arm} {ARM_DESC[arm]} | {m}/{n} | {p1:.3f} | {p3:.3f} | {rd} |')

# ---- speed among CORRECT runs only
P('\n## Speed and cost among CORRECT runs only (multi-repo, arm vs A1), because skipped work is not speed\n')
P('| change | arm | n correct (A1/arm) | PRs A1 -> arm | turnaround s median A1 -> arm | tokens k A1 -> arm | turnaround diff [95% CI] |')
P('|---|---|---|---|---|---|---|')
for ch in ('C2', 'C3'):
    base = [x for x in main if x['layout'] == 'multi' and x['change'] == ch and x['arm'] == 'A1' and x['passed']]
    for arm in ('A2', 'A3', 'A4', 'A5', 'A6', 'A7'):
        g = [x for x in main if x['layout'] == 'multi' and x['change'] == ch and x['arm'] == arm and x['passed']]
        if not g or not base: P(f'| {ch} | {arm} | {len(base)}/{len(g)} | (no correct runs) | | | |'); continue
        lo, hi = boot_diff([x['turnaround_s'] for x in g], [x['turnaround_s'] for x in base])
        P(f"| {ch} | {arm} {ARM_DESC[arm]} | {len(base)}/{len(g)} | {f(mean([x['prs'] for x in base]))} -> {f(mean([x['prs'] for x in g]))} | {f(med([x['turnaround_s'] for x in base]),0)} -> {f(med([x['turnaround_s'] for x in g]),0)} | {f(mean([x['agent_tokens'] for x in base])/1000,0)} -> {f(mean([x['agent_tokens'] for x in g])/1000,0)} | [{f(lo,0)}, {f(hi,0)}] |")
P('\nThe same comparison for the monorepo (all runs were correct there):\n')
P('| change | arm | PRs A1 -> arm | turnaround s median A1 -> arm | tokens k A1 -> arm | turnaround diff [95% CI] |')
P('|---|---|---|---|---|---|')
for ch in ('C2', 'C3'):
    base = [x for x in main if x['layout'] == 'mono' and x['change'] == ch and x['arm'] == 'A1']
    for arm in ('A2', 'A3', 'A4', 'A5', 'A6', 'A7'):
        g = [x for x in main if x['layout'] == 'mono' and x['change'] == ch and x['arm'] == arm]
        if not g or not base: continue
        lo, hi = boot_diff([x['turnaround_s'] for x in g], [x['turnaround_s'] for x in base])
        P(f"| {ch} | {arm} {ARM_DESC[arm]} | {f(mean([x['prs'] for x in base]))} -> {f(mean([x['prs'] for x in g]))} | {f(med([x['turnaround_s'] for x in base]),0)} -> {f(med([x['turnaround_s'] for x in g]),0)} | {f(mean([x['agent_tokens'] for x in base])/1000,0)} -> {f(mean([x['agent_tokens'] for x in g])/1000,0)} | [{f(lo,0)}, {f(hi,0)}] |")

P('\n## Excluded runs\n')
P(f'{len(excluded)} excluded; first few: ' + ', '.join(f'{n}({fin},{err})' for n, fin, err in excluded[:6]))
txt = '\n'.join(out)
open(f'{R}/analysis.md', 'w').write(txt)
print(txt)
