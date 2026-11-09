# Phase 3 analysis: 17 repositories against 5 (change C3, Sonnet)

Valid runs: 60 at 17 repositories; controls at 5 repositories: 120 (phase 1/2, not concurrent).

## Misses and exploration

| arm | layout | repos | n | runs with a miss | mean repos cloned | cloned the hidden repo | Fisher p (17 vs 5) |
|---|---|---|---|---|---|---|---|
| A1 open / none | multi | 5 | 5 | 0/5 | 5.0 | 5/5 | - |
| A1 open / none | multi | 17 | 5 | 0/5 | 15.4 | 5/5 | 1.000 |
| A1 open / none | mono | 5 | 5 | 0/5 | 1.2 | 0/5 | - |
| A1 open / none | mono | 17 | 5 | 0/5 | 1.0 | 0/5 | 1.000 |
| A2 structured / partial | multi | 5 | 5 | 4/5 | 3.4 | 2/5 | - |
| A2 structured / partial | multi | 17 | 5 | 5/5 | 3.8 | 4/5 | 1.000 |
| A2 structured / partial | mono | 5 | 5 | 0/5 | 1.0 | 0/5 | - |
| A2 structured / partial | mono | 17 | 5 | 0/5 | 1.0 | 0/5 | 1.000 |
| A3 structured / complete | multi | 5 | 5 | 0/5 | 4.0 | 5/5 | - |
| A3 structured / complete | multi | 17 | 5 | 0/5 | 4.0 | 5/5 | 1.000 |
| A3 structured / complete | mono | 5 | 5 | 0/5 | 1.0 | 0/5 | - |
| A3 structured / complete | mono | 17 | 5 | 0/5 | 1.0 | 0/5 | 1.000 |
| A5 open / catalog complete | multi | 5 | 5 | 0/5 | 5.0 | 5/5 | - |
| A5 open / catalog complete | multi | 17 | 5 | 0/5 | 11.6 | 5/5 | 1.000 |
| A5 open / catalog complete | mono | 5 | 5 | 0/5 | 1.2 | 0/5 | - |
| A5 open / catalog complete | mono | 17 | 5 | 0/5 | 1.0 | 0/5 | 1.000 |
| A6 open / catalog stale | multi | 5 | 5 | 0/5 | 4.8 | 5/5 | - |
| A6 open / catalog stale | multi | 17 | 5 | 0/5 | 10.8 | 5/5 | 1.000 |
| A6 open / catalog stale | mono | 5 | 5 | 0/5 | 1.0 | 0/5 | - |
| A6 open / catalog stale | mono | 17 | 5 | 0/5 | 1.2 | 0/5 | 1.000 |
| B4 partial + "others may be affected" | multi | 5 | 5 | 0/5 | 4.2 | 5/5 | - |
| B4 partial + "others may be affected" | multi | 17 | 5 | 0/5 | 5.6 | 5/5 | 1.000 |
| B4 partial + "others may be affected" | mono | 5 | 5 | 0/5 | 1.0 | 0/5 | - |
| B4 partial + "others may be affected" | mono | 17 | 5 | 0/5 | 1.0 | 0/5 | 1.000 |

## Cost of the larger estate (all runs, 17 vs 5)

| arm | layout | tokens k: 5 -> 17 | turnaround s median: 5 -> 17 | turnaround diff [95% CI] | PRs 5 -> 17 |
|---|---|---|---|---|---|
| A1 open / none | multi | 379 -> 293 | 161 -> 135 | [-72, -8] | 4.0 -> 4.0 |
| A1 open / none | mono | 242 -> 310 | 59 -> 68 | [-11, 12] | 1.0 -> 1.0 |
| A2 structured / partial | multi | 344 -> 384 | 127 -> 122 | [-25, 16] | 3.2 -> 3.0 |
| A2 structured / partial | mono | 313 -> 294 | 79 -> 71 | [-22, 2] | 1.0 -> 1.0 |
| A3 structured / complete | multi | 389 -> 367 | 148 -> 126 | [-91, 22] | 4.0 -> 4.0 |
| A3 structured / complete | mono | 302 -> 289 | 60 -> 68 | [-5, 11] | 1.0 -> 1.0 |
| A5 open / catalog complete | multi | 320 -> 372 | 115 -> 124 | [-10, 44] | 4.0 -> 4.0 |
| A5 open / catalog complete | mono | 271 -> 265 | 73 -> 69 | [-11, 15] | 1.0 -> 1.0 |
| A6 open / catalog stale | multi | 329 -> 365 | 146 -> 131 | [-18, 17] | 4.0 -> 4.0 |
| A6 open / catalog stale | mono | 256 -> 273 | 67 -> 59 | [-9, 6] | 1.0 -> 1.0 |
| B4 partial + "others may be affected" | multi | 350 -> 379 | 142 -> 133 | [-33, 11] | 4.0 -> 4.0 |
| B4 partial + "others may be affected" | mono | 302 -> 307 | 63 -> 77 | [-10, 18] | 1.0 -> 1.0 |