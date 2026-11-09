# Phases 8 and 9 (change C3, Sonnet): epics and noisy tickets

Valid runs: phase 8 30, phase 9 30, phase-1 controls used 30.

| arm | layout | n | complete (all three apps live, right values) | runs with an app left unfixed | runs with a wrong owner value | opened the hidden repo | repos cloned | PRs | turnaround s (median) | tokens k (mean) | cost $ | child tickets opened / closed | epic closes refused |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 clean open-ended (control) | multi | 5 | 5/5 | 0/5 | 0/5 | 5/5 | 5.0 | 4.0 | 161 | 379 | 0.13 | 0.0 / 0.0 | 0 |
| A1 clean open-ended (control) | mono | 5 | 5/5 | 0/5 | 0/5 | 0/5 | 1.2 | 1.0 | 59 | 242 | 0.09 | 0.0 / 0.0 | 0 |
| A2 single ticket, partial list (control) | multi | 5 | 1/5 | 4/5 | 0/5 | 2/5 | 3.4 | 3.2 | 127 | 344 | 0.12 | 0.0 / 0.0 | 0 |
| A2 single ticket, partial list (control) | mono | 5 | 5/5 | 0/5 | 0/5 | 0/5 | 1.0 | 1.0 | 79 | 313 | 0.13 | 0.0 / 0.0 | 0 |
| A3 single ticket, complete list (control) | multi | 5 | 5/5 | 0/5 | 0/5 | 5/5 | 4.0 | 4.0 | 148 | 389 | 0.12 | 0.0 / 0.0 | 0 |
| A3 single ticket, complete list (control) | mono | 5 | 5/5 | 0/5 | 0/5 | 0/5 | 1.0 | 1.0 | 60 | 302 | 0.12 | 0.0 / 0.0 | 0 |
| E1 epic, children without reports | multi | 5 | 3/5 | 1/5 | 1/5 | 5/5 | 4.2 | 3.8 | 150 | 424 | 0.13 | 2.6 / 3.0 | 0 |
| E1 epic, children without reports | mono | 5 | 4/5 | 0/5 | 1/5 | 0/5 | 1.0 | 1.0 | 61 | 321 | 0.13 | 1.8 / 3.0 | 0 |
| E2 epic, children incl. reports | multi | 5 | 5/5 | 0/5 | 0/5 | 5/5 | 4.0 | 4.0 | 166 | 420 | 0.14 | 2.6 / 4.0 | 0 |
| E2 epic, children incl. reports | mono | 5 | 5/5 | 0/5 | 0/5 | 0/5 | 1.0 | 1.6 | 65 | 377 | 0.14 | 2.0 / 4.0 | 0 |
| E3 epic, partial + final "verify" child | multi | 5 | 5/5 | 0/5 | 0/5 | 5/5 | 4.8 | 4.0 | 160 | 483 | 0.15 | 4.0 / 4.0 | 0 |
| E3 epic, partial + final "verify" child | mono | 5 | 3/5 | 0/5 | 2/5 | 0/5 | 1.8 | 1.0 | 60 | 339 | 0.13 | 2.4 / 4.0 | 0 |
| N1 terse | multi | 5 | 4/5 | 1/5 | 0/5 | 5/5 | 5.0 | 4.0 | 122 | 332 | 0.12 | 0.0 / 0.0 | 0 |
| N1 terse | mono | 5 | 5/5 | 0/5 | 0/5 | 0/5 | 2.0 | 1.0 | 65 | 316 | 0.12 | 0.0 / 0.0 | 0 |
| N2 rambling thread | multi | 5 | 0/5 | 5/5 | 0/5 | 5/5 | 5.0 | 4.0 | 125 | 355 | 0.13 | 0.0 / 0.0 | 0 |
| N2 rambling thread | mono | 5 | 0/5 | 5/5 | 0/5 | 0/5 | 2.0 | 1.0 | 62 | 378 | 0.14 | 0.0 / 0.0 | 0 |
| N3 stale library name | multi | 5 | 5/5 | 0/5 | 0/5 | 5/5 | 5.0 | 4.0 | 127 | 338 | 0.12 | 0.0 / 0.0 | 0 |
| N3 stale library name | mono | 5 | 5/5 | 0/5 | 0/5 | 0/5 | 2.0 | 1.0 | 59 | 283 | 0.11 | 0.0 / 0.0 | 0 |

## Misses against the control, multi-repo (Fisher exact)

| arm | misses / n | control | control misses / n | p |
|---|---|---|---|---|
| E1 epic, children without reports | 2/5 | A2 | 4/5 | 0.524 |
| E2 epic, children incl. reports | 0/5 | A3 | 0/5 | 1.000 |
| E3 epic, partial + final "verify" child | 0/5 | A2 | 4/5 | 0.048 |
| N1 terse | 1/5 | A1 | 0/5 | 1.000 |
| N2 rambling thread | 5/5 | A1 | 0/5 | 0.008 |
| N3 stale library name | 0/5 | A1 | 0/5 | 1.000 |

## Cost against the control (multi-repo, all runs)

| arm | control | tokens k: control -> arm | turnaround s median: control -> arm | turnaround diff [95% CI] |
|---|---|---|---|---|
| E1 | A2 | 344 -> 424 | 127 -> 150 | [2, 49] |
| E2 | A3 | 389 -> 420 | 148 -> 166 | [-66, 48] |
| E3 | A2 | 344 -> 483 | 127 -> 160 | [19, 55] |
| N1 | A1 | 379 -> 332 | 161 -> 122 | [-93, -24] |
| N2 | A1 | 379 -> 355 | 161 -> 125 | [-87, -19] |
| N3 | A1 | 379 -> 338 | 161 -> 127 | [-81, -17] |