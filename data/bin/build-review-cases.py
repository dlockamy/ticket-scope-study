#!/usr/bin/env python3
"""Phase 5: build review cases from saved phase 1-4 runs (multi-repo, change C3). Truth is stored OUTSIDE the case dirs.
usage: build-review-cases.py"""
import json, glob, os, random, shutil, subprocess, re
R = os.path.expanduser('~/study-mfe/s2/results'); OUT = '/tmp/s2-review'; TRUTH = os.path.expanduser('~/study-mfe/s2/review/truth.json')
REPO = {'contracts': 'libs-shared-contracts', 'billing': 'apps-sub-route-billing', 'shell': 'apps-core-shell', 'reports': 'apps-sub-route-reports', 'platformkit': 'libs-platform-kit'}
runs = []
for f in sorted(glob.glob(f'{R}/s[2345]-C3-*-multi-r*/summary.json')):
    s = json.load(open(f))
    if s.get('agent_error') is True or not (s.get('agent_tokens') or 0): continue
    runs.append((os.path.dirname(f), s))
inc = [r for r in runs if r[1]['missed']]; com = [r for r in runs if not r[1]['missed']]
rng = random.Random(20261030); com = rng.sample(com, 30)
cases = inc + com; rng.shuffle(cases)
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(f'{OUT}/cases'); os.makedirs(f'{OUT}/empty'); os.makedirs(f'{OUT}/out')
# read-only baseline copy of the repositories as they were before any change
S = os.path.expanduser('~/study-mfe/s2/snap/study'); os.makedirs(f'{OUT}/base')
for k, d in (('contracts', 'multi/libs-shared-contracts'), ('billing', 'multi/apps-sub-route-billing'), ('shell', 'multi/apps-core-shell'), ('reports', 'multi/apps-sub-route-reports'), ('platformkit', 'external/libs-platform-kit')):
    subprocess.run(['rsync', '-a', '--exclude', 'node_modules', '--exclude', '.git', f'{S}/{d}/', f'{OUT}/base/{REPO[k]}/'], check=True)
subprocess.run(['chmod', '-R', 'a-w', f'{OUT}/base'], check=True)
truth = {}
for i, (d, s) in enumerate(cases, 1):
    cid = f'c{i:02d}'; cd = f'{OUT}/cases/{cid}'; os.makedirs(cd)
    shutil.copy(f'{d}/ticket.md', f'{cd}/ticket.md')
    parts = []
    for k in ('contracts', 'billing', 'shell', 'reports', 'platformkit'):
        p = f'{d}/landed-{k}.diff'
        if os.path.exists(p) and os.path.getsize(p):
            t = open(p).read()
            t = re.sub(r'^=== (\w+) (.*)$', r'commit \1: \2', t, flags=re.M)
            parts.append(f'##### repository: {REPO[k]}\n{t}')
    open(f'{cd}/change.diff', 'w').write('\n'.join(parts))
    summ = ''
    for l in open(f'{d}/events.jsonl'):
        e = json.loads(l)
        if e['event'] == 'done': summ = e.get('summary', '')
    open(f'{cd}/summary.txt', 'w').write(summ)
    hidden = (s['missed'] or [None])[0]
    names = {'reports': ['reports'], 'shell': ['shell'], None: []}[hidden]
    truth[cid] = dict(run=os.path.basename(d), incomplete=bool(s['missed']), missed=s['missed'], dev_model=s['model'], arm=s['arm'], tag=s['tag'],
                      summary_mentions_hidden=bool(hidden and any(n in summ.lower() for n in names)), hidden_repo_cloned=bool(hidden and hidden in (s.get('repos_cloned') or [])))
json.dump(truth, open(TRUTH, 'w'), indent=1)
print(len(cases), 'cases;', sum(t['incomplete'] for t in truth.values()), 'incomplete; summary mentions hidden app in', sum(t['summary_mentions_hidden'] for t in truth.values() if t['incomplete']), 'of the incomplete')
