#!/usr/bin/env python3
"""Per-run metrics. usage: report.py <run-dir> [end_ms]"""
import json, sys, os, urllib.request
R = sys.argv[1]; J = 'http://127.0.0.1:18080'
meta = json.load(open(f'{R}/meta.json')); start = meta['start_ms']
ev = [json.loads(l) for l in open(f'{R}/events.jsonl')] if os.path.exists(f'{R}/events.jsonl') else []
prs = json.load(open(f'{R}/prs.json')) if os.path.exists(f'{R}/prs.json') else []
tasks = json.load(open(f'{R}/tasks.json')) if os.path.exists(f'{R}/tasks.json') else []
end_ev = [e for e in ev if e['event'] in ('done', 'blocked')]
end = end_ev[-1]['ts'] if end_ev else (int(sys.argv[2]) if len(sys.argv) > 2 else (ev[-1]['ts'] if ev else start))
def get(u):
    try: return json.load(urllib.request.urlopen(J + u, timeout=15))
    except Exception: return {}
jobs = []
keys = ['mono', 'platformkit'] if meta['topology'] == 'mono' else ['shell', 'billing', 'reports', 'contracts', 'platformkit']
names = {'mono': 'mono', 'platformkit': 'ext-platformkit', 'shell': 'multi-shell', 'billing': 'multi-billing', 'reports': 'multi-reports', 'contracts': 'multi-contracts'}
builds = []
for k in keys:
    for kind in ('ci', 'cd'):
        j = f'{names[k]}-{kind}'
        d = get(f'/job/{j}/api/json?tree=jobs[name,builds[number,timestamp,duration,result]]')
        for br in d.get('jobs', []):
            for b in br.get('builds', []):
                if start <= b['timestamp'] <= end + 120000:
                    builds.append(dict(job=j, branch=br['name'], dur=b['duration'], result=b['result']))
ci_events = [e for e in ev if e['event'] == 'ci_result']; dep_events = [e for e in ev if e['event'] == 'deploy_result']
wait_ms = sum(e.get('waited_ms', 0) for e in ci_events + dep_events)
turn = (end - start) / 1000
first = lambda name: next(((e['ts'] - start) / 1000 for e in ev if e['event'] == name), None)
out = dict(run=meta['run'], topology=meta['topology'], change=meta['change'], arm=meta['arm'], rep=meta['rep'], model=meta['model'], tag=meta['tag'], structure=meta['structure'],
  finished=('done' if any(e['event'] == 'done' for e in ev) else 'blocked' if any(e['event'] == 'blocked' for e in ev) else 'UNFINISHED'),
  turnaround_s=round(turn), jenkins_wait_s=round(wait_ms / 1000), agent_active_s=round(turn - wait_ms / 1000),
  t_first_clone_s=first('clone'), t_first_pr_s=first('pr_opened'), t_first_merge_s=first('pr_merged'),
  repos_cloned=sorted({e['repo'] for e in ev if e['event'] == 'clone'}),
  repos_changed=sorted({p['repo'] for p in prs}),
  prs=len(prs), prs_merged=sum(1 for p in prs if p.get('merged_ts')),
  pr_detail=[dict(id=p['id'], repo=p['repo'], **{k: p['size'].get(k) for k in ('files', 'add', 'del', 'lock_add', 'lock_del', 'commits')}, open_to_merge_s=round((p['merged_ts'] - p['opened_ts']) / 1000) if p.get('merged_ts') else None) for p in prs],
  lines_changed_excl_lock=sum(p['size'].get('add', 0) + p['size'].get('del', 0) for p in prs), files_changed=sum(p['size'].get('files', 0) for p in prs),
  pr_updates=sum(1 for e in ev if e['event'] == 'pr_updated'),
  ci_runs=len(ci_events), ci_failures=sum(1 for e in ci_events if e['result'] != 'SUCCESS'),
  deploys=len(dep_events), deploy_failures=sum(1 for e in dep_events if e['cd_result'] != 'SUCCESS' or e['ci_main_result'] != 'SUCCESS'),
  subtasks_recorded=len(tasks), subtask_detail=[dict(repo=t['repo'], title=t['title']) for t in tasks],
  jenkins_builds=len(builds), jenkins_executor_s=round(sum(b['dur'] for b in builds) / 1000, 1), jenkins_failed_builds=sum(1 for b in builds if b['result'] not in ('SUCCESS',)),
  jenkins_builds_by_job={j: sum(1 for b in builds if b['job'] == j) for j in sorted({b['job'] for b in builds})})

from collections import Counter
per_repo = Counter(p['repo'] for p in prs)
out['deps_queries'] = sum(1 for e in ev if e['event'] == 'deps_query')
out['asks'] = sum(1 for e in ev if e['event'] == 'ask')
out['audit_runs'] = sum(1 for e in ev if e['event'] == 'audit')
out['audit_last_violations'] = next((e.get('violations') for e in reversed(ev) if e['event'] == 'audit'), None)
out['hidden'] = meta.get('hidden')
out['decoy_touched'] = 'platformkit' in out['repos_changed'] and meta['change'] != 'C1'
out['repeat_repo_prs'] = sum(max(0, n - 1) for n in per_repo.values())
out['rework_events'] = out['ci_failures'] + out['pr_updates'] + out['deploy_failures']
out['messages'] = 0
ag = f'{R}/agent.json'
if os.path.exists(ag):
    try:
        a = json.load(open(ag)); u = a.get('usage', {})
        out['agent_tokens'] = u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0) + u.get('output_tokens', 0)
        out['agent_output_tokens'] = u.get('output_tokens', 0); out['agent_turns'] = a.get('num_turns'); out['agent_cost_usd'] = a.get('total_cost_usd'); out['agent_duration_s'] = round(a.get('duration_ms', 0) / 1000)
        out['agent_error'] = a.get('is_error')
    except Exception as e: out['agent_parse_error'] = str(e)
print(json.dumps(out))
