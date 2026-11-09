# Phase 2 analysis (change C3, Sonnet)

Valid runs: 120. New arms (s3): 50; phase-1 controls (s2, C3): 70.

## Misses and behaviour

| arm | layout | n | runs with a miss | cloned the hidden repo | ran `st audit` (runs / last report clean) | used `st ask` | tasks recorded (mean) | vs A2: Fisher p | vs A1: Fisher p |
|---|---|---|---|---|---|---|---|---|---|
| A1 open / none (phase 1) | multi | 5 | 0/5 | 5/5 | 0/5 (0 clean) | 0/5 | 3.2 | 0.048 | - |
| A1 open / none (phase 1) | mono | 5 | 0/5 | 0/5 | 0/5 (0 clean) | 0/5 | 2.0 | 1.000 | - |
| A2 structured / partial (phase 1) | multi | 5 | 4/5 | 2/5 | 0/5 (0 clean) | 0/5 | 0.0 | - | 0.048 |
| A2 structured / partial (phase 1) | mono | 5 | 0/5 | 0/5 | 0/5 (0 clean) | 0/5 | 0.0 | - | 1.000 |
| A3 structured / complete (phase 1) | multi | 5 | 0/5 | 5/5 | 0/5 (0 clean) | 0/5 | 0.0 | 0.048 | 1.000 |
| A3 structured / complete (phase 1) | mono | 5 | 0/5 | 0/5 | 0/5 (0 clean) | 0/5 | 0.0 | 1.000 | 1.000 |
| A5 open / catalog (phase 1) | multi | 5 | 0/5 | 5/5 | 0/5 (0 clean) | 0/5 | 4.0 | 0.048 | 1.000 |
| A5 open / catalog (phase 1) | mono | 5 | 0/5 | 0/5 | 0/5 (0 clean) | 0/5 | 2.0 | 1.000 | 1.000 |
| B1 partial + "find every app" instruction | multi | 5 | 0/5 | 5/5 | 0/5 (0 clean) | 0/5 | 1.0 | 0.048 | 1.000 |
| B1 partial + "find every app" instruction | mono | 5 | 0/5 | 0/5 | 0/5 (0 clean) | 0/5 | 1.2 | 1.000 | 1.000 |
| B2 partial + global audit check | multi | 5 | 0/5 | 5/5 | 5/5 (5 clean) | 0/5 | 0.0 | 0.048 | 1.000 |
| B2 partial + global audit check | mono | 5 | 0/5 | 0/5 | 5/5 (5 clean) | 0/5 | 0.0 | 1.000 | 1.000 |
| B3 partial + st ask available | multi | 5 | 4/5 | 4/5 | 0/5 (0 clean) | 0/5 | 0.0 | 1.000 | 0.048 |
| B3 partial + st ask available | mono | 5 | 0/5 | 0/5 | 0/5 (0 clean) | 0/5 | 0.0 | 1.000 | 1.000 |
| B4 partial + "others may be affected" | multi | 5 | 0/5 | 5/5 | 0/5 (0 clean) | 0/5 | 0.0 | 0.048 | 1.000 |
| B4 partial + "others may be affected" | mono | 5 | 0/5 | 0/5 | 0/5 (0 clean) | 0/5 | 0.0 | 1.000 | 1.000 |
| A2s partial, hidden = core-shell | multi | 5 | 2/5 | 3/5 | 0/5 (0 clean) | 0/5 | 0.0 | 0.524 | 0.444 |
| A2s partial, hidden = core-shell | mono | 5 | 0/5 | 0/5 | 0/5 (0 clean) | 0/5 | 0.0 | 1.000 | 1.000 |

## Cost among correct runs only (multi-repo)

| arm | n correct | PRs | turnaround s (median) | tokens k (mean) | turnaround diff vs A2-correct-or-A1 [95% CI] |
|---|---|---|---|---|---|
| A1 open / none (phase 1) | 5 | 4.0 | 161 | 379 | [nan, nan] (vs A1) |
| A3 structured / complete (phase 1) | 5 | 4.0 | 148 | 389 | [-67, 62] (vs A1) |
| A5 open / catalog (phase 1) | 5 | 4.0 | 115 | 320 | [-97, -24] (vs A1) |
| B1 partial + "find every app" instruction | 5 | 4.0 | 136 | 302 | [-74, -3] (vs A1) |
| B2 partial + global audit check | 5 | 4.0 | 164 | 397 | [-51, 23] (vs A1) |
| B3 partial + st ask available | 1 | 4.0 | 146 | 360 | [nan, nan] (vs A1) |
| B4 partial + "others may be affected" | 5 | 4.0 | 142 | 350 | [-65, 5] (vs A1) |
| A2s partial, hidden = core-shell | 3 | 4.0 | 143 | 429 | [-69, 3] (vs A1) |