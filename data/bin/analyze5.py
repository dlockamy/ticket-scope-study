#!/usr/bin/env python3
"""Phase 5 analysis: reviewers (arms V0-V4) on 60 saved cases (30 incomplete, 30 complete). stdlib only. -> results/analysis-phase5.md"""
import json, os, re, math
from math import comb
from collections import defaultdict
B = '/tmp/s2-review'; R = os.path.expanduser('~/study-mfe/s2/results')
truth = json.load(open(os.path.expanduser('~/study-mfe/s2/review/truth.json')))
ARMS = ['V0', 'V1', 'V2', 'V3', 'V4']
DESC = {'V0': 'ticket + diff', 'V1': 'ticket + diff + can look at the repos', 'V2': 'V1 + checklist line', 'V3': 'ticket + diff + true list of apps', 'V4': "ticket + diff + developer's summary"}
NAME = {'reports': r'report', 'shell': r'shell'}
res = {}   # (case, arm) -> dict
bad = []
for c in truth:
    for a in ARMS:
        p = f'{B}/out/{c}-{a}.json'
        if not os.path.exists(p): continue
        j = json.load(open(p))
        if j.get('terminal_reason') != 'completed': bad.append((c, a, j.get('terminal_reason'))); continue
        txt = j.get('result') or ''
        m = re.search(r'\{.*\}', txt, re.S); v = None; issues = []; conf = None
        if m:
            try:
                o = json.loads(m.group(0)); v = o.get('verdict'); issues = o.get('issues') or []; conf = o.get('confidence')
            except Exception: pass
        if v not in ('approve', 'request_changes'): bad.append((c, a, 'unparsable')); continue
        u = j.get('usage') or {}
        tok = (u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0) + u.get('output_tokens', 0))
        itext = ' '.join(f"{i.get('where','')} {i.get('problem','')}" for i in issues if isinstance(i, dict))
        t = truth[c]
        named = bool(t['incomplete'] and re.search(NAME[t['missed'][0]], itext, re.I))
        res[(c, a)] = dict(verdict=v, issues=len(issues), caught=int(t['incomplete'] and v == 'request_changes' and named), flagged_other=int(t['incomplete'] and v == 'request_changes' and not named),
                           false_alarm=int((not t['incomplete']) and v == 'request_changes'), tokens=tok, cost=j.get('total_cost_usd') or 0, turns=j.get('num_turns'), itext=itext)
inc = [c for c in truth if truth[c]['incomplete']]; com = [c for c in truth if not truth[c]['incomplete']]
def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 2
    p = k / n; d = 1 + z * z / n; ce = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return ce - h, ce + h
def sign(b, c):
    n = b + c
    if n == 0: return 1.0
    k = min(b, c); return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)
o = []; P = o.append
P('# Phase 5 analysis: reviewers on saved cases\n')
P(f'Cases: {len(inc)} incomplete, {len(com)} complete. Reviews completed: {len(res)} of {len(truth) * len(ARMS)}; unusable (error or unparsable): {len(bad)}.\n')
P('## Catch rate and false alarms\n')
P('| arm | reviewer sees | named the missing app and requested changes (of 30 incomplete) [95% CI] | requested changes, any reason | approved an incomplete change | false alarms on complete (of 30) | tokens k (mean) | cost $ (mean) |')
P('|---|---|---|---|---|---|---|---|')
for a in ARMS:
    I = [res[(c, a)] for c in inc if (c, a) in res]; C = [res[(c, a)] for c in com if (c, a) in res]
    k = sum(r['caught'] for r in I); lo, hi = wilson(k, len(I))
    allr = I + C
    P(f"| {a} | {DESC[a]} | {k}/{len(I)} ({100*k/max(1,len(I)):.0f}%) [{100*lo:.0f}%, {100*hi:.0f}%] | {sum(r['caught']+r['flagged_other'] for r in I)}/{len(I)} | {sum(1 for r in I if r['verdict']=='approve')} | {sum(r['false_alarm'] for r in C)}/{len(C)} | {sum(r['tokens'] for r in allr)/max(1,len(allr))/1000:.0f} | {sum(r['cost'] for r in allr)/max(1,len(allr)):.3f} |")
P('\n## Paired comparison with V0 (same cases): exact sign test on catches\n')
P('| arm | caught by arm but not V0 | caught by V0 but not arm | p |')
P('|---|---|---|---|')
for a in ARMS[1:]:
    b = sum(1 for c in inc if res.get((c, a), {}).get('caught') and not res.get((c, 'V0'), {}).get('caught')); d = sum(1 for c in inc if res.get((c, 'V0'), {}).get('caught') and not res.get((c, a), {}).get('caught'))
    P(f'| {a} | {b} | {d} | {('< 0.0001' if sign(b, d) < 0.0001 else format(sign(b, d), '.4f'))} |')
P('\n## Catch rate by what the developer wrote and did\n')
P('| arm | summary named the missing app (n=%d): caught | summary did not name it (n=%d): caught | developer opened the hidden repo (n=%d): caught | never opened it (n=%d): caught | developer was main model (n=%d): caught | smaller model (n=%d): caught |' % (
    sum(truth[c]['summary_mentions_hidden'] for c in inc), sum(not truth[c]['summary_mentions_hidden'] for c in inc), sum(truth[c]['hidden_repo_cloned'] for c in inc), sum(not truth[c]['hidden_repo_cloned'] for c in inc),
    sum(truth[c]['dev_model'] != 'haiku' for c in inc), sum(truth[c]['dev_model'] == 'haiku' for c in inc)))
P('|---|---|---|---|---|---|---|')
def frac(a, f):
    s = [c for c in inc if f(truth[c])]; return f"{sum(res.get((c, a), {}).get('caught', 0) for c in s)}/{len(s)}"
for a in ARMS:
    P(f"| {a} | {frac(a, lambda t: t['summary_mentions_hidden'])} | {frac(a, lambda t: not t['summary_mentions_hidden'])} | {frac(a, lambda t: t['hidden_repo_cloned'])} | {frac(a, lambda t: not t['hidden_repo_cloned'])} | {frac(a, lambda t: t['dev_model'] != 'haiku')} | {frac(a, lambda t: t['dev_model'] == 'haiku')} |")
P('\n## What false alarms were about (sample of issue text, complete cases)\n')
n = 0
for a in ARMS:
    for c in com:
        r = res.get((c, a))
        if r and r['false_alarm'] and n < 10: P(f"* {a} {c}: {r['itext'][:230]}"); n += 1
txt = '\n'.join(o); open(f'{R}/analysis-phase5.md', 'w').write(txt); print(txt)
