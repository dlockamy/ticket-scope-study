#!/usr/bin/env python3
"""Emit the two per-run tables for claim-check.md (verbatim quotes from the `st done` summaries). stdlib only."""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load import load_runs
R = load_runs(); single = [r for r in R if r['tag'] not in ('s6', 's7')]
inc = sorted([r for r in single if r['tag'] in ('s2', 's2h', 's3', 's4', 's5') and r['topology'] == 'multi' and not r['acceptance_pass']], key=lambda r: r['_name'])
def done(r):
    t = ''
    for l in open(r['_dir'] + '/events.jsonl'):
        e = json.loads(l)
        if e['event'] == 'done': t = e.get('summary', '')
    return t
def quote(r):
    pat = 'shell' if r['missed'][0] == 'shell' else r'report'
    out = []
    for x in re.split(r'(?<=\.)\s+', done(r).replace('\n', ' ')):
        m = re.search(pat, x, re.I)
        if not m: continue
        x = x.strip()
        if len(x) > 330:
            a = max(0, m.start() - 90); x = ('...' if a else '') + x[a:a + 300] + '...'
        out.append(x)
    return ' '.join(out)
CAT = {  # hand-read categories for the 21 that never cloned it
 's2-C2-A7-multi-r2': 'says it did not clone it', 's2-C2-A7-multi-r3': 'asserts it is unaffected; no check (wrong)',
 's2-C3-A2-multi-r1': 'asserts it does not call validateApp; no check (wrong)', 's2-C3-A2-multi-r2': 'says not in ticket and not checked',
 's2-C3-A2-multi-r3': 'says not cloned or checked', 's2-C3-A4-multi-r2': 'says not touched and unaffected; no check stated',
 's2-C3-A4-multi-r4': 'says it did not clone it', 's2-C3-A4-multi-r5': 'says not in ticket and not touched',
 's2-C3-A7-multi-r1': 'asserts it does not call validateApp; no check (wrong)', 's2-C3-A7-multi-r3': 'asserts it does not call validateApp; no check (wrong)',
 's2-C3-A7-multi-r4': 'says not in ticket and not checked', 's2h-C3-A4-multi-r1': 'no mention', 's3-C3-A2s-multi-r3': 'no mention',
 's3-C3-A2s-multi-r4': 'asserts the shell does not call validateApp; no check (wrong)', 's3-C3-B3-multi-r3': 'says not in scope and unaffected; no check stated',
 's4-C3-A2-multi-r2': 'does not name it; says other repos were not checked', 's5-C3-A2-multi-r1': 'no mention', 's5-C3-A2-multi-r2': 'no mention',
 's5-C3-A2-multi-r3': 'no mention', 's5-C3-A2-multi-r4': 'no mention', 's5-C3-B2-multi-r3': 'learned of it from the audit command; reported it as open'}
SCOPE_NO = {'s2-C3-A7-multi-r2', 's3-C3-B3-multi-r4'}
cl = [r for r in inc if r['missed'][0] in r['repos_cloned']]; nc = [r for r in inc if r['missed'][0] not in r['repos_cloned']]
esc = lambda s: s.replace('|', '\\|')
print('### Table A: the 12 that cloned the missing app\'s repository\n')
print('| Run | Cloned it? | PR on it? | What the `st done` summary says (verbatim) | Verdict |')
print('|---|---|---|---|---|')
for r in cl:
    v = 'Confirmed, weaker: names it as unchanged and pinned, no scope reason in this summary (the final message gives one)' if r['_name'] in SCOPE_NO else 'Confirmed'
    print(f"| {r['_name']} | yes | no | \"{esc(quote(r))}\" | {v} |")
print('\n### Table B: the 21 that never cloned it\n')
print('| Run | Cloned it? | What the `st done` summary says (verbatim, or category) | Category | Verdict on \"never looked\" |')
print('|---|---|---|---|---|')
assert len(nc) == 21 and set(CAT) == {r['_name'] for r in nc}, (len(nc), set(CAT) ^ {r['_name'] for r in nc})
for r in nc:
    q = quote(r)
    print(f"| {r['_name']} | no | {('\"' + esc(q) + '\"') if q else '(no mention)'} | {CAT[r['_name']]} | Confirmed: no clone event |")
