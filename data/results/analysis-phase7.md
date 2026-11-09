# Phase 6: two developers, one ticket (change C3, complete list, Sonnet)

Valid runs: 30 (agents ran without an API error; a developer who never signalled done is counted as a timeout).

| condition | layout | n | complete | merge conflicts (mean) | PRs (mean) | PR updates | CI failures | makespan s (median) | timeouts | free messages | handoff notes posted / read | dev-b waiting on the other dev, s (mean) | tokens k (mean) | cost $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H0 no channel | multi | 5 | 5/5 | 0.0 | 4.0 | 0.0 | 0 | 478 | 0 | 0.0 | 0 / 0 | 0 | 605 | 0.21 |
| H1 free messages | multi | 5 | 5/5 | 0.0 | 4.0 | 0.0 | 0 | 97 | 0 | 1.8 | 0 / 0 | 39 | 647 | 0.22 |
| H2 required handoff note | multi | 5 | 5/5 | 0.0 | 4.0 | 0.0 | 0 | 106 | 0 | 0.0 | 5 / 37 | 0 | 578 | 0.20 |
| H0 no channel | mono | 5 | 5/5 | 0.0 | 3.2 | 0.0 | 0 | 94 | 0 | 0.0 | 0 / 0 | 0 | 711 | 0.28 |
| H1 free messages | mono | 5 | 5/5 | 0.0 | 2.8 | 0.0 | 0 | 91 | 0 | 2.2 | 0 / 0 | 35 | 743 | 0.29 |
| H2 required handoff note | mono | 5 | 5/5 | 0.0 | 3.0 | 0.2 | 0 | 95 | 0 | 0.0 | 5 / 37 | 0 | 731 | 0.29 |

## Release class chosen by dev-a, and slow adoption by dev-b (multi-repo)

| condition | classes chosen (major / minor / patch / none) | dev-b finished after 300 s | dev-b finish s (sorted) | dev-b merge after contract live, s (sorted) |
|---|---|---|---|---|
| H0 no channel | 1 / 3 / 1 / 0 | 4/5 | [100.2, 464.0, 478.2, 683.4, 689.9] | [24.8, 389.2, 403.1, 598.1, 599.3] |
| H1 free messages | 2 / 3 / 0 / 0 | 0/5 | [85.9, 93.5, 95.1, 97.1, 99.4] | [23.7, 24.9, 26.0, 26.3, 26.6] |
| H2 required handoff note | 3 / 1 / 1 / 0 | 0/5 | [85.4, 98.2, 106.3, 112.5, 116.1] | [27.7, 31.0, 32.6, 36.3, 36.8] |

## Completeness: pairwise (Fisher exact, multi-repo)

| comparison | complete / n (first) | complete / n (second) | p |
|---|---|---|---|
| H0 vs H1 | 5/5 | 5/5 | 1.000 |
| H0 vs H2 | 5/5 | 5/5 | 1.000 |
| H1 vs H2 | 5/5 | 5/5 | 1.000 |

## Incomplete or odd runs
