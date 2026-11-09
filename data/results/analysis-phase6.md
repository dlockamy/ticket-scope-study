# Phase 6: two developers, one ticket (change C3, complete list, Sonnet)

Valid runs: 30 (agents ran without an API error; a developer who never signalled done is counted as a timeout).

| condition | layout | n | complete | merge conflicts (mean) | PRs (mean) | PR updates | CI failures | makespan s (median) | timeouts | free messages | handoff notes posted / read | dev-b waiting on the other dev, s (mean) | tokens k (mean) | cost $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H0 no channel | multi | 5 | 5/5 | 0.0 | 4.0 | 0.0 | 0 | 106 | 0 | 0.0 | 0 / 0 | 0 | 728 | 0.24 |
| H1 free messages | multi | 5 | 5/5 | 0.0 | 4.0 | 0.0 | 0 | 99 | 0 | 1.6 | 0 / 0 | 33 | 613 | 0.21 |
| H2 required handoff note | multi | 5 | 5/5 | 0.0 | 4.0 | 0.0 | 0 | 98 | 0 | 0.0 | 5 / 34 | 0 | 655 | 0.22 |
| H0 no channel | mono | 5 | 5/5 | 0.0 | 2.6 | 0.0 | 0 | 90 | 0 | 0.0 | 0 / 0 | 0 | 679 | 0.26 |
| H1 free messages | mono | 5 | 5/5 | 0.0 | 2.6 | 0.4 | 0 | 84 | 0 | 2.6 | 0 / 0 | 4 | 749 | 0.28 |
| H2 required handoff note | mono | 5 | 5/5 | 0.0 | 2.8 | 0.2 | 0 | 93 | 0 | 0.0 | 5 / 21 | 0 | 700 | 0.26 |

## Release class chosen by dev-a, and slow adoption by dev-b (multi-repo)

| condition | classes chosen (major / minor / patch / none) | dev-b finished after 300 s | dev-b finish s (sorted) | dev-b merge after contract live, s (sorted) |
|---|---|---|---|---|
| H0 no channel | 5 / 0 / 0 / 0 | 1/5 | [89.3, 93.0, 98.5, 105.7, 610.7] | [22.1, 24.5, 24.8, 25.8, 552.9] |
| H1 free messages | 5 / 0 / 0 / 0 | 0/5 | [87.5, 88.7, 91.7, 107.8, 108.1] | [24.8, 25.4, 25.4, 25.6, 27.2] |
| H2 required handoff note | 5 / 0 / 0 / 0 | 0/5 | [86.5, 96.0, 97.6, 101.0, 103.9] | [22.9, 23.6, 26.5, 27.6, 29.4] |

## Completeness: pairwise (Fisher exact, multi-repo)

| comparison | complete / n (first) | complete / n (second) | p |
|---|---|---|---|
| H0 vs H1 | 5/5 | 5/5 | 1.000 |
| H0 vs H2 | 5/5 | 5/5 | 1.000 |
| H1 vs H2 | 5/5 | 5/5 | 1.000 |

## Incomplete or odd runs
