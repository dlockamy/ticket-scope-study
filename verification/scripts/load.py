"""Shared loader. Read-only on the data directory. stdlib only."""
import json, os, glob
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'results')
def load_runs():
    runs = []
    for d in sorted(glob.glob(ROOT + '/s*-*')):
        base = os.path.basename(d)
        sj = os.path.join(d, 'summary.json')
        if not os.path.isfile(sj):
            continue
        try:
            s = json.load(open(sj))
        except Exception:
            continue
        s['_dir'] = d
        s['_name'] = base
        runs.append(s)
    return runs
def agent(d):
    try:
        return json.load(open(os.path.join(d, 'agent.json')))
    except Exception:
        return {}
