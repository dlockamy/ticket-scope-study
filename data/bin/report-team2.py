#!/usr/bin/env python3
"""Team-run metrics. usage: report-team.py <run-dir>"""
import json, sys, os, urllib.request, statistics as st
R = sys.argv[1]; J = 'http://127.0.0.1:18080'
meta = json.load(open(f'{R}/meta.json')); start = meta['start_ms']; devs = meta['devs']
ev = [json.loads(l) for l in open(f'{R}/events.jsonl')]
prs = json.load(open(f'{R}/prs.json')) if os.path.exists(f'{R}/prs.json') else []
msgs = [json.loads(l) for l in open(f'{R}/msgs.jsonl')] if os.path.exists(f'{R}/msgs.jsonl') else []
fin = {d: next((e['ts'] for e in ev if e['who'] == d and e['event'] in ('done', 'blocked')), None) for d in devs}
blocked = [d for d in devs if any(e['who'] == d and e['event'] == 'blocked' for e in ev)]
first_ev0 = min(e['ts'] for e in ev)
timeouts = [d for d in devs if not fin[d]]
end = max([t for t in fin.values() if t] + ([first_ev0 + 1500000] if timeouts else []) or [ev[-1]['ts']])
S = lambda ms: round(ms / 1000, 1)
first_ev = min(e['ts'] for e in ev)
per = {}
for d in devs:
    mine = [e for e in ev if e['who'] == d]
    jw = sum(e.get('waited_ms', 0) for e in mine if e['event'] in ('ci_result', 'deploy_result'))
    cw = sum(e.get('waited_ms', 0) for e in mine if e['event'] == 'msg_wait')
    span = (fin[d] or end) - start
    first = next((e['ts'] for e in mine if e['event'] in ('clone', 'ticket_claimed')), None)
    per[d] = dict(finished_s=S(span), jenkins_wait_s=S(jw), comm_wait_s=S(cw), busy_s=S(span - jw - cw), utilisation=round((span - jw - cw) / span, 2) if span else None,
                  prs=sum(1 for p in prs if p.get('author') == d), msgs_sent=sum(1 for e in mine if e['event'] == 'msg_sent'),
                  clones=sorted({e['repo'] for e in mine if e['event'] == 'clone'}))
reads = [e['latency_ms'] for e in ev if e['event'] == 'msg_read']
out = dict(timeouts=timeouts, run=meta['run'], topology=meta['topology'], mode=meta['mode'], arm=meta['arm'], rep=meta['rep'], tag=meta['tag'], devs=devs, makespan_s=S(end - start), start_offset_s=S(first_ev - start), makespan_from_first_action_s=S(end - first_ev), blocked=blocked, per_dev=per,
  prs=len(prs), prs_merged=sum(1 for p in prs if p.get('merged_ts')), pr_updates=sum(1 for e in ev if e['event'] == 'pr_updated'),
  ci_runs=sum(1 for e in ev if e['event'] == 'ci_result'), ci_failures=sum(1 for e in ev if e['event'] == 'ci_result' and e['result'] != 'SUCCESS'),
  merge_conflicts=sum(1 for e in ev if e['event'] == 'merge_failed'), infra_retries=sum(1 for e in ev if e['event'] == 'infra_retry'),
  msgs_total=len(msgs), msg_chars=sum(len(m['text']) for m in msgs), msg_read_latency_median_s=S(st.median(reads)) if reads else None,
  lines_changed_excl_lock=sum(p['size'].get('add', 0) + p['size'].get('del', 0) for p in prs),
  pr_detail=[dict(id=p['id'], author=p.get('author'), repo=p['repo'], files=p['size'].get('files'), lines=p['size'].get('add', 0) + p['size'].get('del', 0), opened_s=S(p['opened_ts'] - start), merged_s=S(p['merged_ts'] - start) if p.get('merged_ts') else None) for p in prs])
if meta['mode'] == 'team':
    dep = next((e for e in ev if e['event'] == 'deploy_result' and e['who'] == devs[0] and e['cd_result'] == 'SUCCESS'), None)
    b_merge = next((e for e in ev if e['event'] == 'pr_merged' and e['who'] == devs[1]), None)
    out['dependency_live_s'] = S(dep['ts'] - start) if dep else None
    out['dependent_merged_s'] = S(b_merge['ts'] - start) if b_merge else None
    out['handoff_to_dependent_merge_s'] = S(b_merge['ts'] - dep['ts']) if dep and b_merge else None
else:
    tk = {}
    for e in ev:
        if e['event'] == 'ticket_claimed': tk.setdefault(e['ticket'], {})['claimed'] = e['ts']; tk[e['ticket']]['by'] = e['who']
        if e['event'] == 'ticket_done': tk.setdefault(e['ticket'], {})['done'] = e['ts']
    out['tickets'] = {k: dict(by=v.get('by'), claimed_s=S(v['claimed'] - start) if 'claimed' in v else None, done_s=S(v['done'] - start) if 'done' in v else None, cycle_s=S(v['done'] - v['claimed']) if 'done' in v and 'claimed' in v else None) for k, v in sorted(tk.items())}
    out['tickets_done'] = sum(1 for v in tk.values() if 'done' in v)
    out['tickets_per_hour'] = round(out['tickets_done'] / ((end - first_ev) / 3600000), 1)
# Jenkins work in the window
keys = ['mono', 'platformkit'] if meta['topology'] == 'mono' else ['shell', 'billing', 'reports', 'contracts', 'platformkit']
names = {'mono': 'mono', 'platformkit': 'ext-platformkit', 'shell': 'multi-shell', 'billing': 'multi-billing', 'reports': 'multi-reports', 'contracts': 'multi-contracts'}
b = []
for k in keys:
    for kind in ('ci', 'cd'):
        try: d = json.load(urllib.request.urlopen(f'{J}/job/{names[k]}-{kind}/api/json?tree=jobs[name,builds[number,timestamp,duration,result]]', timeout=15))
        except Exception: continue
        for br in d.get('jobs', []):
            for x in br.get('builds', []):
                if start <= x['timestamp'] <= end + 120000: b.append(x)
out['jenkins_builds'] = len(b); out['jenkins_failed_builds'] = sum(1 for x in b if x['result'] != 'SUCCESS'); out['jenkins_executor_s'] = round(sum(x['duration'] for x in b) / 1000, 1)

out['handoffs_posted'] = sum(1 for e in ev if e['event'] == 'handoff_posted'); out['handoff_reads'] = sum(1 for e in ev if e['event'] == 'handoff_read')
out['handoff_reads_empty'] = sum(1 for e in ev if e['event'] == 'handoff_read' and e.get('empty'))
out['msg_waits'] = sum(1 for e in ev if e['event'] == 'msg_wait')
out['dev_b_comm_wait_s'] = per['dev-b']['comm_wait_s']; out['dev_b_jenkins_wait_s'] = per['dev-b']['jenkins_wait_s']; out['dev_b_finished_s'] = per['dev-b']['finished_s']
out['duplicate_clones'] = sum(1 for k in set(c for d in devs for c in per[d]['clones']) if all(k in per[d]['clones'] for d in devs))
tot = 0; cost = 0.0; err = []
for d in devs:
    p = f'{R}/agent-{d}.json'
    try:
        a = json.load(open(p)); u = a.get('usage', {}); tot += u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0) + u.get('output_tokens', 0); cost += a.get('total_cost_usd') or 0
        if a.get('is_error') or a.get('terminal_reason') not in ('completed', None): err.append(d)
    except Exception:
        if d not in timeouts: err.append(d)
out['agent_tokens'] = tot; out['agent_cost_usd'] = round(cost, 4); out['agent_errors'] = err
print(json.dumps(out))
