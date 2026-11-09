#!/usr/bin/env python3
"""Round queue for the screening phase. 16 rounds per replicate (each round = one cell run in BOTH layouts at once).
Replicate-major, shuffled within a replicate (fixed seed), so stopping at any point leaves a balanced design."""
import random, json
cells = [('C1', 'A1'), ('C1', 'A3')] + [('C2', f'A{i}') for i in range(1, 8)] + [('C3', f'A{i}') for i in range(1, 8)]
q = []
for rep in (1, 2, 3, 4, 5):
    r = random.Random(20261030 + rep); c = cells[:]; r.shuffle(c)
    q += [dict(change=ch, arm=a, rep=rep, model='claude-sonnet-5-5', tag='s2') for ch, a in c]
# second-model subset (smaller model), after the first three Sonnet replicates
h = random.Random(7); sub = [('C2', 'A1'), ('C2', 'A3'), ('C2', 'A4'), ('C2', 'A6'), ('C3', 'A1'), ('C3', 'A3'), ('C3', 'A4'), ('C3', 'A6')]; h.shuffle(sub)
hq = [dict(change=ch, arm=a, rep=1, model='haiku', tag='s2h') for ch, a in sub]
out = q[:48] + hq + q[48:]
json.dump(out, open('../queue.json', 'w'), indent=0)
print(len(out), 'rounds;', len(out) * 2, 'runs')
