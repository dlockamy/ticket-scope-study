#!/usr/bin/env python3
"""Recompute the draft's headline numbers from the raw per-run results. stdlib only. Read-only on the data.
usage: python3 -I recompute.py > ../recompute-output.txt
"""
import sys, os, json, re, glob, statistics as stt
from math import comb
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load import ROOT, load_runs, agent

DATA = os.path.dirname(ROOT)
R = load_runs()
def P(*a): print(*a)
def fisher(a, n1, b, n2):
    """two-sided Fisher exact p for a/n1 vs b/n2 (sum of tables no more likely than observed)"""
    K = a + b; N = n1 + n2
    def pr(x): return comb(n1, x) * comb(n2, K - x) / comb(N, K)
    p0 = pr(a)
    return sum(pr(x) for x in range(max(0, K - n2), min(n1, K) + 1) if pr(x) <= p0 * (1 + 1e-9))
def valid(s): return s.get('agent_error') is not True and (s.get('agent_tokens') or 0) > 0 and s.get('finished') in ('done', 'blocked')

P('# A. Run counts and cost'); P()
single = [r for r in R if r['tag'] not in ('s6', 's7')]
team = [r for r in R if r['tag'] in ('s6', 's7')]
P('single-developer runs:', len(single), '| team runs:', len(team), '| review files:', len(glob.glob(DATA + '/review/out/*.json')))
bytag = defaultdict(float); ntag = Counter()
for r in R: bytag[r['tag']] += r.get('agent_cost_usd') or 0; ntag[r['tag']] += 1
rev_cost = sum(json.load(open(f)).get('total_cost_usd') or 0 for f in glob.glob(DATA + '/review/out/*.json'))
P('cost by tag:', {k: round(v, 2) for k, v in sorted(bytag.items())})
P('phase 1 (s2+s2h):', round(bytag['s2'] + bytag['s2h'], 2), '| reviews:', round(rev_cost, 2))
tot = sum(bytag.values()) + rev_cost
P('TOTAL cost, dev runs + reviews:', round(tot, 4))
invalid = [r['_name'] for r in single if not valid(r)]
P('single-developer runs failing the study validity test (agent_error / no tokens / not done|blocked):', len(invalid), invalid[:5])
# cost basis
cb = Counter()
for r in single[:400]:
    for m, u in (agent(r['_dir']).get('modelUsage') or {}).items(): cb[(m, u.get('costBasis'))] += 1
P('modelUsage models / costBasis seen in agent.json (single-dev runs):', dict(cb))
ci = sum(r.get('ci_failures') or 0 for r in single); P('CI failures, single-dev runs:', ci, 'of', len(single), '| team runs ci_failures:', sum(r.get('ci_failures') or 0 for r in team))
P('single-dev runs in phases 1-4:', len([r for r in single if r['tag'] in ('s2', 's2h', 's3', 's4', 's5')]), '(draft section 6 says 326 single-developer runs for the zero-CI-failure claim; there are', len(single), 'single-developer runs in all)')

P(); P('# B. Section 3.1: layout cost (phase 1, main model s2, all arms pooled)'); P()
s2 = [r for r in R if r['tag'] == 's2']
for ch in ('C1', 'C2', 'C3'):
    row = []
    for key in ('prs', 'jenkins_builds', 'turnaround_s'):
        m = [r[key] for r in s2 if r['change'] == ch and r['topology'] == 'mono']; u = [r[key] for r in s2 if r['change'] == ch and r['topology'] == 'multi']
        agg = stt.mean  # the draft's 3.1 table uses means (analysis.md rows 50-64)
        row.append(f'{key}: mono {agg(m):.1f} multi {agg(u):.1f} (n {len(m)},{len(u)})')
    P(ch, ' | '.join(row), '| turnaround median mono/multi:', stt.median([r['turnaround_s'] for r in s2 if r['change']==ch and r['topology']=='mono']), stt.median([r['turnaround_s'] for r in s2 if r['change']==ch and r['topology']=='multi']))

P(); P('# C. Variance shares (sequential SS: layout, change, arm, layout x arm, layout x change), main model s2')
def decompose(rows, o):
    ys = [r[o] for r in rows]; mu = sum(ys) / len(ys); sst = sum((y - mu) ** 2 for y in ys)
    resid = [y - mu for y in ys]; res = {}
    for name, kf in (('layout', lambda r: r['topology']), ('change', lambda r: r['change']), ('arm', lambda r: r['arm']), ('layout x arm', lambda r: (r['topology'], r['arm'])), ('layout x change', lambda r: (r['topology'], r['change']))):
        g = defaultdict(list)
        for r, e in zip(rows, resid): g[kf(r)].append(e)
        fit = {k: sum(v) / len(v) for k, v in g.items()}
        res[name] = sum(len(v) * fit[k] ** 2 for k, v in g.items()) / sst
        resid = [e - fit[kf(r)] for r, e in zip(rows, resid)]
    res['residual'] = sum(e * e for e in resid) / sst
    return res
for o in ('prs', 'jenkins_builds', 'turnaround_s', 'any_miss'):
    rows = [dict(r, any_miss=int(len(r.get('missed') or []) > 0)) for r in s2 if (o != 'any_miss' or r['change'] in ('C2', 'C3'))]
    d = decompose(rows, o); P(o, {k: f'{v*100:.0f}%' for k, v in d.items()})
# order check: layout entered LAST
def layout_last_share(rows, o):
    ys = [r[o] for r in rows]; mu = sum(ys) / len(ys); sst = sum((y - mu) ** 2 for y in ys)
    resid = [y - mu for y in ys]
    for kf in (lambda r: r['change'], lambda r: r['arm'], lambda r: (r['change'], r['arm']), lambda r: r['topology']):
        g = defaultdict(list)
        for r, e in zip(rows, resid): g[kf(r)].append(e)
        fit = {k: sum(v) / len(v) for k, v in g.items()}
        last = sum(len(v) * fit[k] ** 2 for k, v in g.items()) / sst
        resid = [e - fit[kf(r)] for r, e in zip(rows, resid)]
    return last
P('layout share when entered AFTER change, arm and change x arm (order check):', {o: f'{layout_last_share(s2, o)*100:.0f}%' for o in ('prs', 'jenkins_builds', 'turnaround_s')})
cells = Counter((r['change'], r['arm'], r['topology']) for r in s2); P('s2 cell sizes (min/max):', min(cells.values()), max(cells.values()), '- balanced across layouts:', all(cells[(c, a, 'mono')] == cells[(c, a, 'multi')] for c, a, t in cells))

P(); P('# D. Section 3.2: runs with a miss, phase 1 main model (s2)'); P()
for ch in ('C1', 'C2', 'C3'):
    for arm in sorted({r['arm'] for r in s2}):
        a = [r for r in s2 if r['change'] == ch and r['arm'] == arm and r['topology'] == 'mono']; b = [r for r in s2 if r['change'] == ch and r['arm'] == arm and r['topology'] == 'multi']
        if a or b: P(ch, arm, 'mono', sum(not r['acceptance_pass'] for r in a), '/', len(a), '| multi', sum(not r['acceptance_pass'] for r in b), '/', len(b))
c3m = {arm: [r for r in s2 if r['change'] == 'C3' and r['arm'] == arm and r['topology'] == 'multi'] for arm in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7')}
miss = lambda L: sum(not r['acceptance_pass'] for r in L)
P('structured+partial (A2+A4+A7) multi C3:', sum(miss(c3m[a]) for a in ('A2', 'A4', 'A7')), '/', sum(len(c3m[a]) for a in ('A2', 'A4', 'A7')))
P('A1 open-ended multi C3, phase 1:', miss(c3m['A1']), '/', len(c3m['A1']))
for a in ('A2', 'A4', 'A7'): P(f'Fisher {a} vs A1:', round(fisher(miss(c3m[a]), 5, 0, 5), 3))
a1all = [r for r in single if r['topology'] == 'multi' and r['change'] == 'C3' and r['arm'] == 'A1']
P('A1 open-ended multi C3, every phase and model:', {t: f"{miss([r for r in a1all if r['tag']==t])}/{len([r for r in a1all if r['tag']==t])}" for t in sorted({r['tag'] for r in a1all})})
open_like = [r for r in single if r['topology'] == 'multi' and r['change'] == 'C3' and r['tag'] in ('s2', 's3', 's4', 's5', 's2h') and r['arm'] in ('A1', 'A3', 'A5', 'A6')]
P('A1,A3,A5,A6 multi C3, phases 1-4 all models:', miss(open_like), '/', len(open_like))

P(); P('# E. Monorepo misses'); P()
for grp, tags in (('phases 1-4', ('s2', 's2h', 's3', 's4', 's5')), ('phases 8-9b', ('s8', 's9', 's9b')), ('phases 6-7 (team)', ('s6', 's7'))):
    m = [r for r in R if r['topology'] == 'mono' and r['tag'] in tags]
    P(grp, 'mono runs:', len(m), 'failing the scorer:', sum(not r['acceptance_pass'] for r in m))
for r in R:
    if r['topology'] == 'mono' and r['tag'] in ('s8', 's9', 's9b') and not r['acceptance_pass']:
        cons = {k: (v.get('src_ok'), v.get('live_ok')) for k, v in r['consumers'].items()}
        P('  mono failure', r['_name'], 'repos_changed', r.get('repos_changed'), 'consumers(src_ok,live_ok)', cons)

P(); P('# F. Section 3.3: the 33 incomplete multi-repo changes in phases 1-4')
P4 = ('s2', 's2h', 's3', 's4', 's5')
inc = [r for r in single if r['tag'] in P4 and r['topology'] == 'multi' and not r['acceptance_pass']]
P('count:', len(inc), 'by phase tag:', dict(Counter(r['tag'] for r in inc)))
rows = []
for r in inc:
    hid = r['missed'][0]; opened = hid in r['repos_cloned']
    res = agent(r['_dir']).get('result') or ''
    rows.append((r, hid, opened, res))
P('hidden repo cloned (st clone event):', sum(o for _, _, o, _ in rows), '| never cloned:', sum(not o for _, _, o, _ in rows))
P('missed app other than reports:', [r['_name'] for r, h, _, _ in rows if h != 'reports'])
P('changed a PR on the hidden repo (repos_changed contains it):', [r['_name'] for r, h, _, _ in rows if h in (r.get('repos_changed') or [])])
mention = lambda res, h: bool(re.search(h, res, re.I))
P('final summary names the hidden app (keyword), of 33:', sum(mention(res, h) for _, h, _, res in rows))
P('  of the 12 that cloned it:', sum(mention(res, h) for _, h, o, res in rows if o), '| of the 21 that did not:', sum(mention(res, h) for _, h, o, res in rows if not o))
P('review truth file: incomplete cases', sum(1 for v in json.load(open(DATA + '/review/truth.json')).values() if v['incomplete']))
tr = json.load(open(DATA + '/review/truth.json'))
inc_names = {r['_name'] for r in inc}; truth_names = {v['run'] for v in tr.values() if v['incomplete']}
P('  in the 33 but not in the 30 review cases:', sorted(inc_names - truth_names), '| in review but not in 33:', sorted(truth_names - inc_names))

P(); P('# G. Per-arm: cloned the hidden repo vs finished (multi-repo, C3) - feeds figure (b)')
groups = [('Main model, 5 repos', ('s2', 's3')), ('Main model, 17 repos', ('s4',)), ('Smaller model, 5 repos', ('s5',))]
for label, tags in groups:
    P(label)
    arms = sorted({r['arm'] for r in single if r['tag'] in tags and r['change'] == 'C3' and r['topology'] == 'multi'})
    for arm in arms:
        L = [r for r in single if r['tag'] in tags and r['arm'] == arm and r['change'] == 'C3' and r['topology'] == 'multi']
        hid = lambda r: ('shell' if r['arm'] == 'A2s' else 'reports')
        opened = sum(hid(r) in r['repos_cloned'] for r in L); fin = sum(r['acceptance_pass'] for r in L)
        P(f'   {arm}: n={len(L)} cloned hidden={opened} finished={fin}')
P('smaller model phase-1 subset (s2h) multi C3 per arm:', {a: f"{sum(r['acceptance_pass'] for r in single if r['tag']=='s2h' and r['change']=='C3' and r['arm']==a and r['topology']=='multi')}/{len([r for r in single if r['tag']=='s2h' and r['change']=='C3' and r['arm']==a and r['topology']=='multi'])}" for a in ('A1', 'A3', 'A4', 'A6')})

P(); P('# H. B1/B4 cost vs the open-ended arm (multi-repo, C3, main model)')
def stats(tag, arm, key, agg=stt.mean, lay='multi', ch='C3'):
    return agg([r[key] for r in single if r['tag'] == tag and r['arm'] == arm and r['topology'] == lay and r['change'] == ch])
for arm, tag in (('A1', 's2'), ('A2', 's2'), ('A3', 's2'), ('B1', 's3'), ('B2', 's3'), ('B4', 's3')):
    P(arm, 'tokens mean', round(stats(tag, arm, 'agent_tokens')), '| turnaround median', stats(tag, arm, 'turnaround_s', stt.median), '| correct runs only:', sum(r['acceptance_pass'] for r in single if r['tag'] == tag and r['arm'] == arm and r['topology'] == 'multi' and r['change'] == 'C3'))
P('Smaller model multi C3 tokens (mean): ', {arm: round(stats('s5', arm, 'agent_tokens')) for arm in ('A1', 'A2', 'B1', 'B2', 'B4')})
P('single-developer A3 multi C3 turnaround median (draft says 148 s):', stats('s2', 'A3', 'turnaround_s', stt.median))

P(); P('# I. Clarification channel (arm B3)')
n_ask_runs = 0; asks = 0
for r in single:
    if r['tag'] in ('s2', 's2h', 's3', 's4', 's5', 's8', 's9', 's9b'):
        m = json.load(open(r['_dir'] + '/meta.json'))
        if m.get('clarify'): n_ask_runs += 1; asks += r.get('asks', 0)
P('runs where the ask command existed:', n_ask_runs, '| questions asked:', asks, "| draft says 'no question asked in 25 runs'")

P(); P('# J. Phase 5 reviews (re-scored from review/out)')
NAME_LOOSE = {'reports': r'report', 'shell': r'shell'}; NAME_STRICT = {'reports': r'sub-route-reports|\breports\b', 'shell': r'core-shell|\bshell\b'}
ARMS = ['V0', 'V1', 'V2', 'V3', 'V4']
def score(namemap):
    out = {}
    for a in ARMS:
        caught = req = appr = fa = 0
        for c, t in tr.items():
            j = json.load(open(f'{DATA}/review/out/{c}-{a}.json')); txt = j.get('result') or ''
            m = re.search(r'\{.*\}', txt, re.S); o = json.loads(m.group(0)); v = o['verdict']; issues = o.get('issues') or []
            it = ' '.join(f"{i.get('where','')} {i.get('problem','')}" for i in issues if isinstance(i, dict))
            if t['incomplete']:
                named = bool(re.search(namemap[t['missed'][0]], it, re.I))
                caught += int(v == 'request_changes' and named); req += int(v == 'request_changes'); appr += int(v == 'approve')
            else: fa += int(v == 'request_changes')
        out[a] = (caught, req, appr, fa)
    return out
P('arm: (caught, asked for changes, approved incomplete, false alarms on 30 complete)')
P('  as the study scored it (loose regex):', score(NAME_LOOSE))
P('  stricter regex (whole word / repo name):', score(NAME_STRICT))
inc_cases = [c for c, t in tr.items() if t['incomplete']]
smn = [c for c in inc_cases if tr[c]['summary_mentions_hidden']]
P('incomplete cases whose developer summary mentions the hidden app (keyword):', len(smn), 'of', len(inc_cases))
# V4 breakdown
def v4(c):
    j = json.load(open(f'{DATA}/review/out/{c}-V4.json')); o = json.loads(re.search(r'\{.*\}', j['result'], re.S).group(0)); return o['verdict']
P('V4 asked for changes where summary mentions (of %d):' % len(smn), sum(v4(c) == 'request_changes' for c in smn), '| approved:', sum(v4(c) == 'approve' for c in smn))

P(); P('# K. Phase 7 (judgement-call release), multi-repo')
for tag in ('s6', 's7'):
    for arm in ('H0', 'H1', 'H2'):
        L = sorted([r for r in team if r['tag'] == tag and r['arm'] == arm and r['topology'] == 'multi'], key=lambda r: r['rep'])
        P(tag, arm, 'complete', sum(r['acceptance_pass'] for r in L), '/', len(L), '| dev-b finish s', [round(r['dev_b_finished_s']) for r in L], '| makespan median', round(stt.median(r['makespan_s'] for r in L)), '| classes', dict(Counter(r['semver_class'] for r in L)))
h0 = [r['dev_b_finished_s'] for r in team if r['tag'] == 's7' and r['arm'] == 'H0' and r['topology'] == 'multi']
oth = [r['dev_b_finished_s'] for r in team if r['tag'] == 's7' and r['arm'] != 'H0' and r['topology'] == 'multi']
slow0 = sum(x > 300 for x in h0); slowo = sum(x > 300 for x in oth)
P('Fisher H0 (slow %d/%d) vs H1+H2 (slow %d/%d): p = %.4f' % (slow0, len(h0), slowo, len(oth), fisher(slow0, len(h0), slowo, len(oth))))
H1 = [r['dev_b_finished_s'] for r in team if r['tag'] == 's7' and r['arm'] == 'H1' and r['topology'] == 'multi']
P('Fisher H0 vs H1 alone: p = %.4f' % fisher(slow0, 5, sum(x > 300 for x in H1), 5))
P('extra minutes over the median of the other ten:', [round((x - stt.median(oth)) / 60, 1) for x in h0 if x > 300], '| other ten range', round(min(oth)), round(max(oth)), 'median', round(stt.median(oth)))
P('dev-b finished: slow H0 range', round(min(x for x in h0 if x > 300)), round(max(h0)))
P('team runs complete (all): ', sum(r['acceptance_pass'] for r in team), '/', len(team))

P(); P('# L. Section 5 prediction tally: sum of the table columns (hand-entered in the draft)')
rows5 = {'1': (8, 4, 2, 0, 2), '2': (7, 5, 0, 2, 0), '3': (7, 3, 1, 3, 0), '4': (5, 4, 1, 0, 0), '5': (7, 4, 0, 2, 1), '6': (6, 0, 1, 3, 2), '7': (5, 5, 0, 0, 0), '8': (5, 2, 2, 1, 0), '9': (5, 0, 2, 3, 0), '9b': (3, 3, 0, 0, 0)}
P('sum (predictions, right, partly, wrong, not testable):', tuple(sum(v[i] for v in rows5.values()) for i in range(5)), '| rows that do not add up:', [k for k, v in rows5.items() if v[0] != sum(v[1:])])
