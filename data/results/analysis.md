# Analysis (s2*)

Valid runs: **176** (main model 160, second model 16). Excluded (agent/auth error or unfinished): 0.
Replicates per cell (main model): min 5, max 5, cells 32.

## Per-cell results (main model)

| change | arm | layout | n | pass | any miss | hidden (reports) missed | PRs | builds | turnaround s (median) | rework | repeat-repo PRs | clones | tokens (k) | cost $ | decoy touched |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | A1 open / none | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 67 | 0.00 | 0.00 | 1.6 | 292 | 0.11 | 0 |
| C1 | A1 open / none | multi | 5 | 5/5 | 0/5 | 0/5 | 2.0 | 8.0 | 87 | 0.00 | 0.00 | 2.0 | 284 | 0.10 | 0 |
| C1 | A3 structured / complete | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 63 | 0.00 | 0.00 | 1.0 | 271 | 0.10 | 0 |
| C1 | A3 structured / complete | multi | 5 | 5/5 | 0/5 | 0/5 | 2.0 | 8.0 | 92 | 0.00 | 0.00 | 2.0 | 289 | 0.10 | 0 |
| C2 | A1 open / none | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 65 | 0.00 | 0.00 | 2.0 | 258 | 0.10 | 0 |
| C2 | A1 open / none | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 131 | 0.20 | 0.00 | 5.0 | 267 | 0.10 | 0 |
| C2 | A2 structured / partial | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 63 | 0.00 | 0.00 | 1.0 | 253 | 0.10 | 0 |
| C2 | A2 structured / partial | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 139 | 0.00 | 0.00 | 4.0 | 318 | 0.11 | 0 |
| C2 | A3 structured / complete | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 66 | 0.00 | 0.00 | 1.0 | 269 | 0.11 | 0 |
| C2 | A3 structured / complete | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 143 | 0.00 | 0.00 | 4.0 | 287 | 0.10 | 0 |
| C2 | A4 structured / decoy | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 68 | 0.00 | 0.00 | 2.0 | 263 | 0.11 | 0 |
| C2 | A4 structured / decoy | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 146 | 0.20 | 0.00 | 5.0 | 329 | 0.11 | 0 |
| C2 | A5 open / catalog complete | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 78 | 0.00 | 0.00 | 2.0 | 279 | 0.10 | 0 |
| C2 | A5 open / catalog complete | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 131 | 0.00 | 0.00 | 5.0 | 267 | 0.10 | 0 |
| C2 | A6 open / catalog stale | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 67 | 0.00 | 0.00 | 2.0 | 217 | 0.08 | 0 |
| C2 | A6 open / catalog stale | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 138 | 0.00 | 0.00 | 5.0 | 284 | 0.10 | 0 |
| C2 | A7 structured+checks / partial | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 58 | 0.00 | 0.00 | 1.0 | 248 | 0.10 | 0 |
| C2 | A7 structured+checks / partial | multi | 5 | 3/5 | 2/5 | 2/5 | 3.6 | 14.4 | 136 | 0.00 | 0.00 | 3.6 | 306 | 0.10 | 0 |
| C3 | A1 open / none | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 59 | 0.00 | 0.00 | 1.2 | 242 | 0.09 | 0 |
| C3 | A1 open / none | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 161 | 0.20 | 0.00 | 5.0 | 379 | 0.13 | 0 |
| C3 | A2 structured / partial | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 79 | 0.00 | 0.00 | 1.0 | 313 | 0.13 | 0 |
| C3 | A2 structured / partial | multi | 5 | 1/5 | 4/5 | 4/5 | 3.2 | 13.0 | 127 | 0.20 | 0.00 | 3.4 | 344 | 0.12 | 0 |
| C3 | A3 structured / complete | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 60 | 0.00 | 0.00 | 1.0 | 302 | 0.12 | 0 |
| C3 | A3 structured / complete | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 148 | 0.00 | 0.00 | 4.0 | 389 | 0.12 | 0 |
| C3 | A4 structured / decoy | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 82 | 0.00 | 0.00 | 2.0 | 367 | 0.15 | 0 |
| C3 | A4 structured / decoy | multi | 5 | 0/5 | 5/5 | 5/5 | 3.0 | 12.0 | 116 | 0.00 | 0.00 | 4.4 | 360 | 0.12 | 0 |
| C3 | A5 open / catalog complete | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 73 | 0.00 | 0.00 | 1.2 | 271 | 0.11 | 0 |
| C3 | A5 open / catalog complete | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 115 | 0.20 | 0.00 | 5.0 | 320 | 0.13 | 0 |
| C3 | A6 open / catalog stale | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 67 | 0.00 | 0.00 | 1.0 | 256 | 0.10 | 0 |
| C3 | A6 open / catalog stale | multi | 5 | 5/5 | 0/5 | 0/5 | 4.0 | 16.0 | 146 | 0.00 | 0.00 | 4.8 | 329 | 0.12 | 0 |
| C3 | A7 structured+checks / partial | mono | 5 | 5/5 | 0/5 | 0/5 | 1.0 | 4.0 | 76 | 0.00 | 0.00 | 1.0 | 307 | 0.13 | 0 |
| C3 | A7 structured+checks / partial | multi | 5 | 0/5 | 5/5 | 5/5 | 3.0 | 12.0 | 132 | 0.00 | 0.00 | 3.4 | 383 | 0.12 | 0 |

## Layout effect by change type (all arms pooled, main model)

| change | outcome | monorepo mean | multi-repo mean | diff (multi - mono) [95% boot CI] |
|---|---|---|---|---|
| C1 | any_miss | 0.00 | 0.00 | 0.00 [0.00, 0.00] |
| C1 | prs | 1.00 | 2.00 | 1.00 [1.00, 1.00] |
| C1 | jenkins_builds | 4.00 | 8.00 | 4.00 [4.00, 4.00] |
| C1 | turnaround_s | 67.20 | 91.00 | 23.80 [17.60, 29.70] |
| C1 | rework_events | 0.00 | 0.00 | 0.00 [0.00, 0.00] |
| C1 | n_cloned | 1.30 | 2.00 | 0.70 [0.40, 1.00] |
| C1 | agent_tokens | 281663.80 | 286427.20 | 4763.40 [-25265.50, 33419.20] |
| C2 | any_miss | 0.00 | 0.06 | 0.06 [0.00, 0.14] |
| C2 | prs | 1.00 | 3.94 | 2.94 [2.86, 3.00] |
| C2 | jenkins_builds | 4.00 | 15.77 | 11.77 [11.43, 12.00] |
| C2 | turnaround_s | 66.49 | 138.20 | 71.71 [62.91, 80.74] |
| C2 | rework_events | 0.00 | 0.06 | 0.06 [0.00, 0.14] |
| C2 | n_cloned | 1.57 | 4.51 | 2.94 [2.69, 3.20] |
| C2 | agent_tokens | 255437.14 | 294133.86 | 38696.71 [21740.54, 55288.46] |
| C3 | any_miss | 0.00 | 0.40 | 0.40 [0.23, 0.57] |
| C3 | prs | 1.00 | 3.60 | 2.60 [2.43, 2.77] |
| C3 | jenkins_builds | 4.00 | 14.43 | 10.43 [9.74, 11.09] |
| C3 | turnaround_s | 71.83 | 135.37 | 63.54 [51.11, 77.86] |
| C3 | rework_events | 0.00 | 0.09 | 0.09 [0.00, 0.17] |
| C3 | n_cloned | 1.20 | 4.29 | 3.09 [2.80, 3.37] |
| C3 | agent_tokens | 293962.89 | 357652.11 | 63689.23 [39627.57, 86667.97] |

## Practice vs the open-ended baseline A1 (within layout and change type)

Lower is better for every outcome shown. "Rule" = at least 20% lower AND the 95% interval of the difference excludes zero. HARM = at least 20% higher AND the interval excludes zero.

| change | layout | arm | outcome | A1 mean | arm mean | change % | 95% CI of diff | n (A1/arm) | verdict |
|---|---|---|---|---|---|---|---|---|---|
| C2 | mono | A2 structured / partial | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A2 structured / partial | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A2 structured / partial | turnaround_s | 65.40 | 63.20 | -3 | [-12.20, 7.80] | 5/5 |  |
| C2 | mono | A2 structured / partial | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A2 structured / partial | agent_tokens | 258165.60 | 252574.40 | -2 | [-46057.60, 34527.60] | 5/5 |  |
| C2 | mono | A3 structured / complete | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A3 structured / complete | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A3 structured / complete | turnaround_s | 65.40 | 67.20 | 3 | [-9.20, 13.00] | 5/5 |  |
| C2 | mono | A3 structured / complete | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A3 structured / complete | agent_tokens | 258165.60 | 269403.40 | 4 | [-27954.40, 48741.80] | 5/5 |  |
| C2 | mono | A4 structured / decoy | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A4 structured / decoy | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A4 structured / decoy | turnaround_s | 65.40 | 68.40 | 5 | [-9.80, 15.60] | 5/5 |  |
| C2 | mono | A4 structured / decoy | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A4 structured / decoy | agent_tokens | 258165.60 | 263289.00 | 2 | [-25729.80, 34349.00] | 5/5 |  |
| C2 | mono | A5 open / catalog complete | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A5 open / catalog complete | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A5 open / catalog complete | turnaround_s | 65.40 | 74.40 | 14 | [-3.00, 21.20] | 5/5 |  |
| C2 | mono | A5 open / catalog complete | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A5 open / catalog complete | agent_tokens | 258165.60 | 279354.00 | 8 | [-20283.80, 64828.80] | 5/5 |  |
| C2 | mono | A6 open / catalog stale | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A6 open / catalog stale | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A6 open / catalog stale | turnaround_s | 65.40 | 64.60 | -1 | [-11.40, 10.00] | 5/5 |  |
| C2 | mono | A6 open / catalog stale | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A6 open / catalog stale | agent_tokens | 258165.60 | 216908.60 | -16 | [-88013.60, 4639.40] | 5/5 |  |
| C2 | mono | A7 structured+checks / partial | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A7 structured+checks / partial | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A7 structured+checks / partial | turnaround_s | 65.40 | 62.20 | -5 | [-15.20, 8.40] | 5/5 |  |
| C2 | mono | A7 structured+checks / partial | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | mono | A7 structured+checks / partial | agent_tokens | 258165.60 | 248365.00 | -4 | [-41857.60, 19835.40] | 5/5 |  |
| C2 | multi | A2 structured / partial | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A2 structured / partial | rework_events | 0.20 | 0.00 | -100 | [-0.60, 0.00] | 5/5 | large but interval spans 0 |
| C2 | multi | A2 structured / partial | turnaround_s | 124.80 | 143.60 | 15 | [-6.80, 44.60] | 5/5 |  |
| C2 | multi | A2 structured / partial | prs | 4.00 | 4.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A2 structured / partial | agent_tokens | 267263.00 | 318210.20 | 19 | [6992.60, 96497.00] | 5/5 |  |
| C2 | multi | A3 structured / complete | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A3 structured / complete | rework_events | 0.20 | 0.00 | -100 | [-0.60, 0.00] | 5/5 | large but interval spans 0 |
| C2 | multi | A3 structured / complete | turnaround_s | 124.80 | 159.60 | 28 | [0.20, 73.80] | 5/5 | HARM |
| C2 | multi | A3 structured / complete | prs | 4.00 | 4.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A3 structured / complete | agent_tokens | 267263.00 | 287316.80 | 8 | [-15076.80, 55639.80] | 5/5 |  |
| C2 | multi | A4 structured / decoy | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A4 structured / decoy | rework_events | 0.20 | 0.20 | 0 | [-0.40, 0.40] | 5/5 |  |
| C2 | multi | A4 structured / decoy | turnaround_s | 124.80 | 139.40 | 12 | [-15.20, 43.40] | 5/5 |  |
| C2 | multi | A4 structured / decoy | prs | 4.00 | 4.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A4 structured / decoy | agent_tokens | 267263.00 | 328582.00 | 23 | [23467.00, 96115.60] | 5/5 | HARM |
| C2 | multi | A5 open / catalog complete | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A5 open / catalog complete | rework_events | 0.20 | 0.00 | -100 | [-0.60, 0.00] | 5/5 | large but interval spans 0 |
| C2 | multi | A5 open / catalog complete | turnaround_s | 124.80 | 130.00 | 4 | [-30.60, 44.20] | 5/5 |  |
| C2 | multi | A5 open / catalog complete | prs | 4.00 | 4.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A5 open / catalog complete | agent_tokens | 267263.00 | 267475.80 | 0 | [-32321.80, 32145.00] | 5/5 |  |
| C2 | multi | A6 open / catalog stale | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A6 open / catalog stale | rework_events | 0.20 | 0.00 | -100 | [-0.60, 0.00] | 5/5 | large but interval spans 0 |
| C2 | multi | A6 open / catalog stale | turnaround_s | 124.80 | 133.60 | 7 | [-17.00, 35.80] | 5/5 |  |
| C2 | multi | A6 open / catalog stale | prs | 4.00 | 4.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C2 | multi | A6 open / catalog stale | agent_tokens | 267263.00 | 283979.00 | 6 | [-27281.60, 56891.60] | 5/5 |  |
| C2 | multi | A7 structured+checks / partial | any_miss | 0.00 | 0.40 | n/a | [0.00, 0.80] | 5/5 |  |
| C2 | multi | A7 structured+checks / partial | rework_events | 0.20 | 0.00 | -100 | [-0.60, 0.00] | 5/5 | large but interval spans 0 |
| C2 | multi | A7 structured+checks / partial | turnaround_s | 124.80 | 136.40 | 9 | [-15.20, 38.60] | 5/5 |  |
| C2 | multi | A7 structured+checks / partial | prs | 4.00 | 3.60 | -10 | [-0.80, 0.00] | 5/5 |  |
| C2 | multi | A7 structured+checks / partial | agent_tokens | 267263.00 | 306110.20 | 15 | [-701.60, 79198.40] | 5/5 |  |
| C3 | mono | A2 structured / partial | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A2 structured / partial | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A2 structured / partial | turnaround_s | 64.40 | 78.80 | 22 | [-0.60, 29.40] | 5/5 | large but interval spans 0 |
| C3 | mono | A2 structured / partial | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A2 structured / partial | agent_tokens | 242294.60 | 312666.40 | 29 | [35793.80, 104540.60] | 5/5 | HARM |
| C3 | mono | A3 structured / complete | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A3 structured / complete | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A3 structured / complete | turnaround_s | 64.40 | 62.40 | -3 | [-13.00, 6.80] | 5/5 |  |
| C3 | mono | A3 structured / complete | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A3 structured / complete | agent_tokens | 242294.60 | 301898.20 | 25 | [29681.40, 87842.60] | 5/5 | HARM |
| C3 | mono | A4 structured / decoy | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A4 structured / decoy | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A4 structured / decoy | turnaround_s | 64.40 | 85.00 | 32 | [6.40, 35.80] | 5/5 | HARM |
| C3 | mono | A4 structured / decoy | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A4 structured / decoy | agent_tokens | 242294.60 | 366847.00 | 51 | [78243.20, 180798.20] | 5/5 | HARM |
| C3 | mono | A5 open / catalog complete | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A5 open / catalog complete | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A5 open / catalog complete | turnaround_s | 64.40 | 71.20 | 11 | [-5.60, 17.80] | 5/5 |  |
| C3 | mono | A5 open / catalog complete | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A5 open / catalog complete | agent_tokens | 242294.60 | 270767.00 | 12 | [-15765.00, 76650.00] | 5/5 |  |
| C3 | mono | A6 open / catalog stale | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A6 open / catalog stale | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A6 open / catalog stale | turnaround_s | 64.40 | 64.20 | -0 | [-11.80, 9.40] | 5/5 |  |
| C3 | mono | A6 open / catalog stale | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A6 open / catalog stale | agent_tokens | 242294.60 | 256260.40 | 6 | [-11311.00, 40244.60] | 5/5 |  |
| C3 | mono | A7 structured+checks / partial | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A7 structured+checks / partial | rework_events | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A7 structured+checks / partial | turnaround_s | 64.40 | 76.80 | 19 | [-2.20, 26.00] | 5/5 |  |
| C3 | mono | A7 structured+checks / partial | prs | 1.00 | 1.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C3 | mono | A7 structured+checks / partial | agent_tokens | 242294.60 | 307006.60 | 27 | [29405.40, 106706.20] | 5/5 | HARM |
| C3 | multi | A2 structured / partial | any_miss | 0.00 | 0.80 | n/a | [0.40, 1.00] | 5/5 |  |
| C3 | multi | A2 structured / partial | rework_events | 0.20 | 0.20 | 0 | [-0.60, 0.40] | 5/5 |  |
| C3 | multi | A2 structured / partial | turnaround_s | 170.20 | 121.80 | -28 | [-88.60, -15.80] | 5/5 | RULE MET |
| C3 | multi | A2 structured / partial | prs | 4.00 | 3.20 | -20 | [-1.00, -0.40] | 5/5 |  |
| C3 | multi | A2 structured / partial | agent_tokens | 378712.00 | 343816.60 | -9 | [-87217.60, 16828.20] | 5/5 |  |
| C3 | multi | A3 structured / complete | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | multi | A3 structured / complete | rework_events | 0.20 | 0.00 | -100 | [-0.60, 0.00] | 5/5 | large but interval spans 0 |
| C3 | multi | A3 structured / complete | turnaround_s | 170.20 | 164.20 | -4 | [-67.40, 60.60] | 5/5 |  |
| C3 | multi | A3 structured / complete | prs | 4.00 | 4.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C3 | multi | A3 structured / complete | agent_tokens | 378712.00 | 389372.00 | 3 | [-46849.20, 71718.20] | 5/5 |  |
| C3 | multi | A4 structured / decoy | any_miss | 0.00 | 1.00 | n/a | [1.00, 1.00] | 5/5 |  |
| C3 | multi | A4 structured / decoy | rework_events | 0.20 | 0.00 | -100 | [-0.60, 0.00] | 5/5 | large but interval spans 0 |
| C3 | multi | A4 structured / decoy | turnaround_s | 170.20 | 115.60 | -32 | [-93.20, -26.80] | 5/5 | RULE MET |
| C3 | multi | A4 structured / decoy | prs | 4.00 | 3.00 | -25 | [-1.00, -1.00] | 5/5 | RULE MET |
| C3 | multi | A4 structured / decoy | agent_tokens | 378712.00 | 360115.80 | -5 | [-71955.40, 31341.80] | 5/5 |  |
| C3 | multi | A5 open / catalog complete | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | multi | A5 open / catalog complete | rework_events | 0.20 | 0.20 | 0 | [-0.60, 0.40] | 5/5 |  |
| C3 | multi | A5 open / catalog complete | turnaround_s | 170.20 | 113.60 | -33 | [-96.40, -24.40] | 5/5 | RULE MET |
| C3 | multi | A5 open / catalog complete | prs | 4.00 | 4.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C3 | multi | A5 open / catalog complete | agent_tokens | 378712.00 | 319776.00 | -16 | [-102038.60, -17866.60] | 5/5 |  |
| C3 | multi | A6 open / catalog stale | any_miss | 0.00 | 0.00 | n/a | [0.00, 0.00] | 5/5 |  |
| C3 | multi | A6 open / catalog stale | rework_events | 0.20 | 0.00 | -100 | [-0.60, 0.00] | 5/5 | large but interval spans 0 |
| C3 | multi | A6 open / catalog stale | turnaround_s | 170.20 | 131.40 | -23 | [-79.80, -5.80] | 5/5 | RULE MET |
| C3 | multi | A6 open / catalog stale | prs | 4.00 | 4.00 | 0 | [0.00, 0.00] | 5/5 |  |
| C3 | multi | A6 open / catalog stale | agent_tokens | 378712.00 | 329238.80 | -13 | [-108002.40, 12050.60] | 5/5 |  |
| C3 | multi | A7 structured+checks / partial | any_miss | 0.00 | 1.00 | n/a | [1.00, 1.00] | 5/5 |  |
| C3 | multi | A7 structured+checks / partial | rework_events | 0.20 | 0.00 | -100 | [-0.60, 0.00] | 5/5 | large but interval spans 0 |
| C3 | multi | A7 structured+checks / partial | turnaround_s | 170.20 | 130.80 | -23 | [-82.40, -1.20] | 5/5 | RULE MET |
| C3 | multi | A7 structured+checks / partial | prs | 4.00 | 3.00 | -25 | [-1.00, -1.00] | 5/5 | RULE MET |
| C3 | multi | A7 structured+checks / partial | agent_tokens | 378712.00 | 382533.60 | 1 | [-45750.80, 53041.60] | 5/5 |  |

## Share of variance explained (sequential sums of squares, main model, C2+C3 only for miss outcomes)

Order of entry: layout, change type, arm, layout x arm, layout x change. Order matters when factors are unbalanced; with an incomplete matrix read these as rough shares, not tests.

| outcome | layout | change type | arm (process levers) | layout x arm | layout x change | residual |
|---|---|---|---|---|---|---|
| any_miss | 13% | 7% | 19% | 19% | 7% | 35% |
| n_missed | 13% | 7% | 19% | 19% | 7% | 35% |
| prs | 87% | 5% | 1% | 1% | 4% | 3% |
| jenkins_builds | 87% | 5% | 1% | 1% | 4% | 3% |
| turnaround_s | 60% | 4% | 1% | 1% | 5% | 29% |
| rework_events | 3% | 1% | 3% | 3% | 1% | 90% |
| n_cloned | 74% | 8% | 7% | 2% | 4% | 5% |
| agent_tokens | 17% | 20% | 9% | 2% | 3% | 49% |

## Misses (a consumer not updated and live) by layout and arm

| change | arm | mono: runs with a miss | multi: runs with a miss | mono hidden missed | multi hidden missed |
|---|---|---|---|---|---|
| C2 | A1 | 0/5 | 0/5 | 0/5 | 0/5 |
| C2 | A2 | 0/5 | 0/5 | 0/5 | 0/5 |
| C2 | A3 | 0/5 | 0/5 | 0/5 | 0/5 |
| C2 | A4 | 0/5 | 0/5 | 0/5 | 0/5 |
| C2 | A5 | 0/5 | 0/5 | 0/5 | 0/5 |
| C2 | A6 | 0/5 | 0/5 | 0/5 | 0/5 |
| C2 | A7 | 0/5 | 2/5 | 0/5 | 2/5 |
| C3 | A1 | 0/5 | 0/5 | 0/5 | 0/5 |
| C3 | A2 | 0/5 | 4/5 | 0/5 | 4/5 |
| C3 | A3 | 0/5 | 0/5 | 0/5 | 0/5 |
| C3 | A4 | 0/5 | 5/5 | 0/5 | 5/5 |
| C3 | A5 | 0/5 | 0/5 | 0/5 | 0/5 |
| C3 | A6 | 0/5 | 0/5 | 0/5 | 0/5 |
| C3 | A7 | 0/5 | 5/5 | 0/5 | 5/5 |

## Second model subset

| change | arm | layout | n | pass | any miss | PRs | turnaround s (median) | tokens (k) |
|---|---|---|---|---|---|---|---|---|
| C2 | A1 | mono | 1 | 1/1 | 0/1 | 1.0 | 83 | 591 |
| C2 | A1 | multi | 1 | 1/1 | 0/1 | 4.0 | 161 | 754 |
| C2 | A3 | mono | 1 | 1/1 | 0/1 | 1.0 | 82 | 802 |
| C2 | A3 | multi | 1 | 1/1 | 0/1 | 4.0 | 1376 | 178 |
| C2 | A4 | mono | 1 | 1/1 | 0/1 | 1.0 | 93 | 783 |
| C2 | A4 | multi | 1 | 1/1 | 0/1 | 4.0 | 227 | 1088 |
| C2 | A6 | mono | 1 | 1/1 | 0/1 | 1.0 | 86 | 602 |
| C2 | A6 | multi | 1 | 1/1 | 0/1 | 4.0 | 177 | 628 |
| C3 | A1 | mono | 1 | 1/1 | 0/1 | 1.0 | 73 | 539 |
| C3 | A1 | multi | 1 | 1/1 | 0/1 | 4.0 | 171 | 1269 |
| C3 | A3 | mono | 1 | 1/1 | 0/1 | 4.0 | 176 | 1001 |
| C3 | A3 | multi | 1 | 1/1 | 0/1 | 4.0 | 206 | 1179 |
| C3 | A4 | mono | 1 | 1/1 | 0/1 | 1.0 | 110 | 788 |
| C3 | A4 | multi | 1 | 0/1 | 1/1 | 3.0 | 154 | 706 |
| C3 | A6 | mono | 1 | 1/1 | 0/1 | 1.0 | 89 | 773 |
| C3 | A6 | multi | 1 | 1/1 | 0/1 | 4.0 | 156 | 1164 |

## Misses: each arm against the references (multi-repo; the monorepo had no misses to test)

Fisher exact, two-sided, on runs with any miss. Reference 1 = A1 (open-ended, no information). Reference 2 = A3 (structured, complete list).

| change | arm | misses / n | vs A1: p | vs A3: p | reading |
|---|---|---|---|---|---|
| C2 | A2 structured / partial | 0/5 | 1.000 | 1.000 | no clear difference from A1 |
| C2 | A3 structured / complete | 0/5 | 1.000 | 1.000 | no clear difference from A1 |
| C2 | A4 structured / decoy | 0/5 | 1.000 | 1.000 | no clear difference from A1 |
| C2 | A5 open / catalog complete | 0/5 | 1.000 | 1.000 | no clear difference from A1 |
| C2 | A6 open / catalog stale | 0/5 | 1.000 | 1.000 | no clear difference from A1 |
| C2 | A7 structured+checks / partial | 2/5 | 0.444 | 0.444 | no clear difference from A1 |
| C3 | A2 structured / partial | 4/5 | 0.048 | 0.048 | more misses than A1 |
| C3 | A3 structured / complete | 0/5 | 1.000 | 1.000 | no clear difference from A1 |
| C3 | A4 structured / decoy | 5/5 | 0.008 | 0.008 | more misses than A1 |
| C3 | A5 open / catalog complete | 0/5 | 1.000 | 1.000 | no clear difference from A1 |
| C3 | A6 open / catalog stale | 0/5 | 1.000 | 1.000 | no clear difference from A1 |
| C3 | A7 structured+checks / partial | 5/5 | 0.008 | 0.008 | more misses than A1 |
| C2+C3 | A2 structured / partial | 4/10 | 0.087 | 0.087 | no clear difference from A1 |
| C2+C3 | A3 structured / complete | 0/10 | 1.000 | 1.000 | no clear difference from A1 |
| C2+C3 | A4 structured / decoy | 5/10 | 0.033 | 0.033 | more misses than A1 |
| C2+C3 | A5 open / catalog complete | 0/10 | 1.000 | 1.000 | no clear difference from A1 |
| C2+C3 | A6 open / catalog stale | 0/10 | 1.000 | 1.000 | no clear difference from A1 |
| C2+C3 | A7 structured+checks / partial | 7/10 | 0.003 | 0.003 | more misses than A1 |

## Speed and cost among CORRECT runs only (multi-repo, arm vs A1), because skipped work is not speed

| change | arm | n correct (A1/arm) | PRs A1 -> arm | turnaround s median A1 -> arm | tokens k A1 -> arm | turnaround diff [95% CI] |
|---|---|---|---|---|---|---|
| C2 | A2 structured / partial | 5/5 | 4.0 -> 4.0 | 131 -> 139 | 267 -> 318 | [-7, 45] |
| C2 | A3 structured / complete | 5/5 | 4.0 -> 4.0 | 131 -> 143 | 267 -> 287 | [0, 74] |
| C2 | A4 structured / decoy | 5/5 | 4.0 -> 4.0 | 131 -> 146 | 267 -> 329 | [-15, 43] |
| C2 | A5 open / catalog complete | 5/5 | 4.0 -> 4.0 | 131 -> 131 | 267 -> 267 | [-31, 44] |
| C2 | A6 open / catalog stale | 5/5 | 4.0 -> 4.0 | 131 -> 138 | 267 -> 284 | [-17, 36] |
| C2 | A7 structured+checks / partial | 5/3 | 4.0 -> 4.0 | 131 -> 136 | 267 -> 317 | [-9, 45] |
| C3 | A2 structured / partial | 5/1 | 4.0 -> 4.0 | 161 -> 87 | 379 -> 304 | [n/a, n/a] |
| C3 | A3 structured / complete | 5/5 | 4.0 -> 4.0 | 161 -> 148 | 379 -> 389 | [-67, 61] |
| C3 | A4 | 5/0 | (no correct runs) | | | |
| C3 | A5 open / catalog complete | 5/5 | 4.0 -> 4.0 | 161 -> 115 | 379 -> 320 | [-96, -24] |
| C3 | A6 open / catalog stale | 5/5 | 4.0 -> 4.0 | 161 -> 146 | 379 -> 329 | [-80, -6] |
| C3 | A7 | 5/0 | (no correct runs) | | | |

The same comparison for the monorepo (all runs were correct there):

| change | arm | PRs A1 -> arm | turnaround s median A1 -> arm | tokens k A1 -> arm | turnaround diff [95% CI] |
|---|---|---|---|---|---|
| C2 | A2 structured / partial | 1.0 -> 1.0 | 65 -> 63 | 258 -> 253 | [-12, 8] |
| C2 | A3 structured / complete | 1.0 -> 1.0 | 65 -> 66 | 258 -> 269 | [-9, 13] |
| C2 | A4 structured / decoy | 1.0 -> 1.0 | 65 -> 68 | 258 -> 263 | [-10, 16] |
| C2 | A5 open / catalog complete | 1.0 -> 1.0 | 65 -> 78 | 258 -> 279 | [-3, 21] |
| C2 | A6 open / catalog stale | 1.0 -> 1.0 | 65 -> 67 | 258 -> 217 | [-11, 10] |
| C2 | A7 structured+checks / partial | 1.0 -> 1.0 | 65 -> 58 | 258 -> 248 | [-15, 8] |
| C3 | A2 structured / partial | 1.0 -> 1.0 | 59 -> 79 | 242 -> 313 | [-1, 29] |
| C3 | A3 structured / complete | 1.0 -> 1.0 | 59 -> 60 | 242 -> 302 | [-13, 7] |
| C3 | A4 structured / decoy | 1.0 -> 1.0 | 59 -> 82 | 242 -> 367 | [6, 36] |
| C3 | A5 open / catalog complete | 1.0 -> 1.0 | 59 -> 73 | 242 -> 271 | [-6, 18] |
| C3 | A6 open / catalog stale | 1.0 -> 1.0 | 59 -> 67 | 242 -> 256 | [-12, 9] |
| C3 | A7 structured+checks / partial | 1.0 -> 1.0 | 59 -> 76 | 242 -> 307 | [-2, 26] |

## Excluded runs

0 excluded; first few: 