# Phase 5 analysis: reviewers on saved cases

Cases: 30 incomplete, 30 complete. Reviews completed: 300 of 300; unusable (error or unparsable): 0.

## Catch rate and false alarms

| arm | reviewer sees | named the missing app and requested changes (of 30 incomplete) [95% CI] | requested changes, any reason | approved an incomplete change | false alarms on complete (of 30) | tokens k (mean) | cost $ (mean) |
|---|---|---|---|---|---|---|---|
| V0 | ticket + diff | 0/30 (0%) [-0%, 11%] | 5/30 | 25 | 2/30 | 6 | 0.018 |
| V1 | ticket + diff + can look at the repos | 27/30 (90%) [74%, 97%] | 27/30 | 3 | 0/30 | 38 | 0.039 |
| V2 | V1 + checklist line | 29/30 (97%) [83%, 99%] | 29/30 | 1 | 0/30 | 32 | 0.035 |
| V3 | ticket + diff + true list of apps | 25/30 (83%) [66%, 93%] | 30/30 | 0 | 0/30 | 6 | 0.018 |
| V4 | ticket + diff + developer's summary | 11/30 (37%) [22%, 54%] | 12/30 | 18 | 6/30 | 6 | 0.020 |

## Paired comparison with V0 (same cases): exact sign test on catches

| arm | caught by arm but not V0 | caught by V0 but not arm | p |
|---|---|---|---|
| V1 | 27 | 0 | < 0.0001 |
| V2 | 29 | 0 | < 0.0001 |
| V3 | 25 | 0 | < 0.0001 |
| V4 | 11 | 0 | 0.0010 |

## Catch rate by what the developer wrote and did

| arm | summary named the missing app (n=24): caught | summary did not name it (n=6): caught | developer opened the hidden repo (n=12): caught | never opened it (n=18): caught | developer was main model (n=25): caught | smaller model (n=5): caught |
|---|---|---|---|---|---|---|
| V0 | 0/24 | 0/6 | 0/12 | 0/18 | 0/25 | 0/5 |
| V1 | 21/24 | 6/6 | 10/12 | 17/18 | 22/25 | 5/5 |
| V2 | 23/24 | 6/6 | 11/12 | 18/18 | 24/25 | 5/5 |
| V3 | 19/24 | 6/6 | 10/12 | 15/18 | 20/25 | 5/5 |
| V4 | 11/24 | 0/6 | 8/12 | 3/18 | 10/25 | 1/5 |

## What false alarms were about (sample of issue text, complete cases)

* V0 c28: apps-sub-route-billing Billing also depends on @studio/platform-kit ^1.0.0, which may itself depend on or call @mfe/shared-contracts ^1. Moving to ^2.0.0 could cause a peer/dependency conflict in the `npm install` prebuild, or mak
* V0 c37: @studio/platform-kit (used by apps-sub-route-billing) The diff doesn't show whether platform-kit calls validateApp or depends on shared-contracts. If it does, it still calls the old signature without an owner and would throw at st
* V4 c01: @studio/platform-kit (used by apps-sub-route-billing) The caller search covered only the cloned repos. platform-kit is a separate package that billing depends on, and it was never checked. If it imports @mfe/shared-contracts and c
* V4 c05: billing, shell, reports (deployment) The description says the apps were 'built locally and deployed'. The ticket's definition of done requires deployment through the normal pipelines, and a local build bypasses that. Nothing shows
* V4 c27: apps-sub-route-billing / @studio/platform-kit Billing also depends on @studio/platform-kit, which is not covered by this change. If it depends on @mfe/shared-contracts and calls validateApp internally without an owner, it will thr
* V4 c45: apps-sub-route-billing / @studio/platform-kit Billing depends on @studio/platform-kit, which was never checked and may call validateApp or depend on shared-contracts itself. A grep of the app repos would not find that caller. If i
* V4 c51: All repositories that consume @mfe/shared-contracts The dependency catalog was already shown to be incomplete, since it omitted reports. The developer found the three callers (shell, billing, reports) from that catalog and does no
* V4 c54: dependency catalog / unidentified consumers of validateApp The developer's own assumption is that the catalog's 3 consumers match a grep of validateApp usage, which was never verified. Any other app or library calling validateApp 