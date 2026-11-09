#!/usr/bin/env python3
"""Second batch of spot checks. stdlib only. Read-only."""
import sys, os, json, re, statistics as stt
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load import ROOT, load_runs, agent
R = load_runs(); single = [r for r in R if r['tag'] not in ('s6', 's7')]; team = [r for r in R if r['tag'] in ('s6', 's7')]
def P(*a): print(*a)
P('# M. Did every open-ended / catalog run clone the hidden repo? (multi-repo, all phases, A1/A5/A6)')
for ch in ('C2', 'C3'):
    L = [r for r in single if r['topology'] == 'multi' and r['change'] == ch and r['arm'] in ('A1', 'A5', 'A6')]
    P(ch, 'runs', len(L), 'cloned reports', sum('reports' in r['repos_cloned'] for r in L), '| cloned all 5 (or all 17 in s4):', sum(len(r['repos_cloned']) >= 5 for r in L))
L = [r for r in single if r['topology'] == 'multi' and r['change'] == 'C3' and r['arm'] in ('A1', 'A5', 'A6') and r['tag'] == 's4']
P('17-repo estate A1/A5/A6 runs:', len(L), 'cloned reports', sum('reports' in r['repos_cloned'] for r in L), 'clones per run', [len(r['repos_cloned']) for r in L])
P(); P('# N. Decoy / catalog / checks (section 3.4)')
P('decoy_touched runs (any):', sum(bool(r.get('decoy_touched')) for r in single if r['tag'] in ('s2', 's2h', 's3', 's4', 's5')))
for lay, ch in (('multi', 'C2'), ('mono', 'C3')):
    a4 = [r['agent_tokens'] for r in single if r['tag'] == 's2' and r['arm'] == 'A4' and r['topology'] == lay and r['change'] == ch]
    a1 = [r['agent_tokens'] for r in single if r['tag'] == 's2' and r['arm'] == 'A1' and r['topology'] == lay and r['change'] == ch]
    P(f'A4 vs A1 tokens, {lay} {ch}: {stt.mean(a4):.0f} vs {stt.mean(a1):.0f} = {100*(stt.mean(a4)/stt.mean(a1)-1):+.0f}%')
q = [r['deps_queries'] for r in single if r['tag'] == 's2' and r['arm'] in ('A5', 'A6') and r['topology'] == 'multi']
P('catalog queries per multi-repo A5/A6 run (phase 1): total', sum(q), 'runs', len(q))
a7 = sum(not r['acceptance_pass'] for r in single if r['tag'] == 's2' and r['arm'] == 'A7' and r['topology'] == 'multi' and r['change'] in ('C2', 'C3'))
a2 = sum(not r['acceptance_pass'] for r in single if r['tag'] == 's2' and r['arm'] == 'A2' and r['topology'] == 'multi' and r['change'] in ('C2', 'C3'))
P('A7 vs A2 misses pooled C2+C3 multi:', a7, '/ 10 vs', a2, '/ 10')
def done_summary(r):
    t = ''
    for l in open(r['_dir'] + '/events.jsonl'):
        e = json.loads(l)
        if e['event'] == 'done': t = e.get('summary', '')
    return t
def final_msg(r): return agent(r['_dir']).get('result') or ''
P4 = ('s2', 's2h', 's3', 's4', 's5')
inc = [r for r in single if r['tag'] in P4 and r['topology'] == 'multi' and not r['acceptance_pass']]
op = [r for r in inc if r['missed'][0] in r['repos_cloned']]; nc = [r for r in inc if r['missed'][0] not in r['repos_cloned']]
P(); P('# O. The 12 that cloned the missing repo: what the closing text says')
P('Two texts exist per run: the `st done` summary (events.jsonl; what the draft quotes and the phase-5 reviewers saw) and the final chat message (agent.json result).')
SCOPE = r'out of scope|wasn.t in the sub-tasks|isn.t in this ticket|not in (the )?(ticket|scope|sub-tasks)|ticket scope|wasn.t in (the )?(ticket|scope)|isn.t in (the )?ticket|doesn.t list|not listed|left out of scope'
P('names the missing app in the done summary:', sum(bool(re.search(r['missed'][0] if False else 'report', done_summary(r), re.I)) for r in op), 'of', len(op))
P('done summary cites scope (out of scope / not in ticket):', sum(bool(re.search(SCOPE, done_summary(r), re.I)) for r in op), 'of', len(op), '| runs that do not:', [r['_name'] for r in op if not re.search(SCOPE, done_summary(r), re.I)])
P('done summary says it stays on ^1.0.0 / is unaffected:', sum(bool(re.search(r'1\.0\.0|unaffected', done_summary(r))) for r in op), 'of', len(op))
P('final message cites scope:', sum(bool(re.search(SCOPE, final_msg(r), re.I)) for r in op), 'of', len(op))
P('says "left it alone" literally (final message):', [r['_name'] for r in op if re.search(r'left it alone', final_msg(r))])
P('opened a PR on the hidden repo:', [r['_name'] for r in op if r['missed'][0] in (r.get('repos_changed') or [])])
P(); P('# P. The 21 that never cloned it: done summary mention (verbatim extracts are in claim-check.md)')
def names(r): return 'shell' if r['missed'][0] == 'shell' else 'report'
P('done summary names the missing app:', sum(bool(re.search(names(r), done_summary(r), re.I)) for r in nc), 'of', len(nc), '| of all 33:', sum(bool(re.search(names(r), done_summary(r), re.I)) for r in inc))
inrev = {v['run'] for v in json.load(open(os.path.dirname(ROOT) + '/review/truth.json')).values() if v['incomplete']}
P('of the 30 phase-5 incomplete cases, done summary names it:', sum(bool(re.search(names(r), done_summary(r), re.I)) for r in inc if r['_name'] in inrev), 'of', len(inrev), '(study truth.json says 24)')
P(); P('# Q. Phase 7 handoff timing (draft: dev-b apps merged 24 to 37 s after the contract was live, H1/H2)')
v = [r['handoff_to_dependent_merge_s'] for r in team if r['tag'] == 's7' and r['topology'] == 'multi' and r['arm'] in ('H1', 'H2') and r.get('handoff_to_dependent_merge_s') is not None]
P('handoff_to_dependent_merge_s (H1+H2 multi, phase 7):', sorted(round(x) for x in v))
v2 = [r.get('dependent_merged_s') for r in team if r['tag'] == 's7' and r['topology'] == 'multi' and r['arm'] in ('H1', 'H2')]
P('dependent_merged_s:', v2)
P(); P('# R. Epic: children closed without being opened (phase 8)')
tot_c = tot_o = tot_u = 0; unread_runs = []; clean = []
for r in single:
    if r['tag'] != 's8': continue
    opened = set(); unop = []; closed = 0
    for l in open(r['_dir'] + '/events.jsonl'):
        e = json.loads(l)
        if e['event'] == 'child_opened': opened.add(e['child'])
        if e['event'] == 'child_done':
            closed += 1
            if e['child'] not in opened: unop.append(e['child'])
    tot_c += closed; tot_u += len(unop)
    (unread_runs if unop else clean).append(r)
P('closed', tot_c, 'closed unopened', tot_u, '| runs closing any child unread:', len(unread_runs), 'of which wrong-owner-value:', sum(1 for r in unread_runs if not r['acceptance_pass'] and not r['missed'] == ['reports']), '| runs that opened every child:', len(clean))
for r in unread_runs + clean:
    pass
wrong = [r['_name'] for r in single if r['tag'] == 's8' and not r['acceptance_pass']]
P('s8 failing runs:', wrong)
P('failing runs among those that opened every child:', [r['_name'] for r in clean if not r['acceptance_pass']])
P(); P('# S. Noisy-ticket totals (phase 9)')
for arm in ('N1', 'N2', 'N3'):
    L = [r for r in single if r['tag'] == 's9' and r['arm'] == arm]; P(arm, 'complete', sum(r['acceptance_pass'] for r in L), '/', len(L))
L = [r for r in single if r['tag'] == 's9']; P('phase 9 all arms failing:', sum(not r['acceptance_pass'] for r in L), 'of', len(L), '| N1+N3 failing:', sum(not r['acceptance_pass'] for r in L if r['arm'] in ('N1', 'N3')), 'of', len([r for r in L if r['arm'] in ('N1', 'N3')]))
L9b = [r for r in single if r['tag'] == 's9b']; P('N2b complete', sum(r['acceptance_pass'] for r in L9b), '/', len(L9b))
P('post-merge breaks (broken_live non-empty) in all runs:', [r['_name'] for r in single if r.get('broken_live')])
