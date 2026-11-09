# Follow-up study: design as executed

> [!info] A standalone first-draft report of this study is in ticket process study. This note is the working log: predictions as written before each phase, scorecards, and deviations.

Executes [the pre-registration](pre-registration.md) overnight, unattended, on 2026-10-29/30, . The 8 predictions and the two starting positions in the prereg are **unchanged**. Outside views: [the outside-sources survey](outside-sources.md). Prior study: [the first study](https://dlockamy.com/posts/2026/11/05/testing-the-monorepo-argument/). Harness and raw data: `~/study-mfe/s2/` (queue `queue.json`, per-run results `results/<run>/`, scorer `bin/accept2.cjs`).

This note was written **before any screening result was read.** Results go in the section at the bottom, added afterwards.

## What was run versus the prereg

| Prereg item | As executed | Why |
|---|---|---|
| Layouts: existing monorepo and multi-repo fields | Rebuilt as field **s2**: same pipelines, plus a **third consumer** of the shared contract (`sub-route-reports`) in both layouts, so F = 3 | The old field had two consumers; the prereg needs three, one hidden |
| L1 ticket structure (3 levels) | open-ended; structured per repository; structured + per-task acceptance checks | as planned |
| L2 dependent information (6 levels) | none; partial list (reports missing); complete; **decoy** (names `libs-platform-kit`, which does not consume, and omits reports); catalog `st deps` complete; catalog stale (reports missing) | as planned |
| Screening design | 7 **arms** A1-A7 (below), not the full L1 x L2 grid | cost; 5 replicates of the full grid is ~540 runs |
| L3 breakdown, L4 clarification, L5 handoff, L6 review input | **Not run in the screening phase.** The scripted requester (`st ask`) and the review harness are built but unused unless time allows | one night; screening first |
| Change types (3) | C1 additive (one consumer uses it); C2 breaking rename reaching all 3 consumers; C3 cross-cutting policy (`validateApp` requires `owner`, each app passes its team from its `package.json`) | as planned |
| Developers | Headless `claude -p` agents, one per run, `--setting-sources project`, no MCP, tools Bash/Read/Edit/Write/Glob/Grep only, fresh session per run. First study used hand-spawned subagents | needed for ~100 unattended runs. Isolation checked (the agent sees none of this vault's instructions) |
| Replicates: 5 per cell | Queue holds up to 5 per cell, **replicate-major, shuffled inside a replicate**, so any stopping point is balanced. How many finished is stated in the results | time |
| Second model | `haiku` on 8 rounds (C2/C3 x A1, A3, A4, A6) inserted after replicate 3 | as planned (subset) |
| Pilot of 12 runs | **One pilot round** (C2/A1, both layouts), archived. Both passed, zero misses. Its timings are void (clock skew, below). No separate 12-run pilot; replicate 1 doubles as the spread estimate | time |

### Arms

| Arm | L1 | L2 |
|---|---|---|
| A1 | open-ended | none |
| A2 | structured per repository | partial (billing, shell) |
| A3 | structured per repository | complete |
| A4 | structured per repository | decoy |
| A5 | open-ended | catalog, complete |
| A6 | open-ended | catalog, stale (reports missing) |
| A7 | structured + acceptance checks | partial |

C1 runs only A1 and A3. Total 16 rounds per replicate; a round runs one cell in both layouts concurrently on the same restored field (separate repos, buckets and Jenkins jobs).

### Scoring (script only)

Acceptance loads the **live deployed bundle** of each of the three apps, the contract as published (multi-repo: from the registry) or on `main` (monorepo), and reports per consumer `src_ok` and `live_ok`. A **miss** is a consumer that is not both. Also: PRs, Jenkins builds, lines, lead time, rework events (CI failures + PR updates + deploy failures), repeat PRs in one repo, a PR on `libs-platform-kit` (decoy touched), clones, `st deps` queries, tokens, turns and cost. The semver class is recorded but is **not** part of pass.

## Deviations and harness faults (recorded as found)

1. **Importmap lost update (field fault).** The shipped `publish.sh` rewrites one shared `importmap.json` read-modify-write. Billing and reports deploying together overwrote each other at baseline. The multi-repo copy now verifies and retries after 2 s. Monorepo untouched (its CD publishes serially). This adds up to ~2 s to each multi-repo app deploy.
2. **Docker VM clock lag.** The VM clock falls about 300 s behind the host at times. With it, every `st pr wait` took ~5 min for a 4 s build (pilot: monorepo 390 s, multi-repo 1327 s, both meaningless). Fixed by a background loop (`bin/clocksync.sh`) that re-syncs every 4 s and logs the skew it found in `results/clock.log`. **Rounds in which a large skew was logged while they ran should have their timings treated with suspicion**; per-run `skew.json` records skew at round start and end.
3. **Hidden consumer is always `reports`.** Chosen for simplicity. App-specific effects cannot be separated from "hidden" effects; they cancel across arms but not across layouts' discoverability.
4. **Decoy is `libs-platform-kit`**, which exists in both layouts and does not consume the contract.
5. **Monorepo CI builds every app on every change** (as shipped), so a missed consumer in C2 fails CI there (`check-contract`), while in C3 nothing at build time catches a missed `owner`. This is a property of the shipped pipeline, not of the layout in general, and it matters for reading prediction 1.
6. **Sample-size caveat made in advance:** published effects of process are small or null in outside evidence ([the outside-sources survey](outside-sources.md)); with 2 to 4 replicates per cell, intervals will be wide and most differences will not clear the 20 percent rule. That outcome is a legitimate result.

## Out of scope (stated deliberately)

Migration, retooling, staffing; access control; human reviewers; **WIP and queueing** (single-ticket runs cannot test them); team handoff (L5) and clarification (L4) are not tested in the screening phase.

## Results

**Screening phase complete: 160 Sonnet runs (80 rounds x 2 layouts, 5 replicates in each of the 32 cells) and 16 smaller-model runs (8 cells x 2 layouts x 1).** Every run was scored by script on the live deployed bundles. Zero runs were excluded after the restart. Data, scripts and the full analysis: `data/README.md` (outside the notes tree; see where the bulk data lives).

### How the night went (read this before trusting any date or count)

* The first matrix (started 00:33) produced **3 usable runs out of 158.** From about 01:17 every headless developer failed instantly with "OAuth session expired and could not be refreshed" and the driver wrote 150-plus empty summaries without noticing, because it counted "a summary exists" rather than "the agent ran". Nothing was wrong with the field or the tickets.
* Fixed in the morning (login pre-flight with retry; a round is valid only if both agents ran without an API error). The invalid summaries were set aside (not deleted, `results/invalid-auth/`) and the **whole queue was re-run from 07:51 to 12:23**. No result in this note comes from the overnight failure; the one overnight round that did run (C2/A4/rep 1) had void timings and was re-run.
* So the study ran about 4.5 hours of real work, not a night's worth, and cost far less than the prereg's 10-million-token estimate (about 61 million tokens counting cache reads, of which 0.59 million were output).

### Headline

1. **A change that crosses a boundary costs the monorepo one PR and four builds, and the multi-repo four PRs and 12 to 16 builds. Layout owns that.** PRs and builds: 87% of the variance is layout. Turnaround 60% (monorepo 66 to 72 s, multi-repo 135 to 138 s on the crossing changes). This confirms the first study and prediction 4.
2. **In the monorepo, no run in 80 missed a consumer, whatever the ticket looked like.** Ticket structure and dependent information changed cost a little (all four structured arms cost 25 to 51% more tokens on the policy change, every interval excluding zero) and nothing else.
3. **In the multi-repo, whether a consumer was missed depended on the ticket, and the direction was the opposite of the common belief.** The policy change (C3) was missed by the hidden consumer in **14 of 15 runs where a structured ticket listed only some consumers** (A2 4/5, A4 5/5, A7 5/5), and in **0 of 20 runs** where the ticket was open-ended (A1), complete (A3) or open-ended with a catalog (A5, A6, even a stale one). Exact test against A1: p = 0.048, 0.008, 0.008.
4. **Mechanism: scope-following.** Open-ended tickets sent the agent to every repository (5.0 clones). A structured ticket told it where the work was, so it stopped looking. Of the 15 runs, **9 never opened the reports repository** (one wrote "reports doesn't call `validateApp`" without checking) and **5 opened it, saw it calls `validateApp`, and left it out because it was not on the ticket**, one writing that it "is out of scope; it stays on ^1.0.0 and will need an owner ('insights') before it upgrades". The acceptance criterion in the same ticket said "every app that calls `validateApp`".
5. **Process matters more than layout for misses; layout matters more than process for speed.** For the miss outcome (C2+C3 runs): layout 13% of variance, ticket arm 19%, layout x arm 19%; the 38% attributable to process is nearly three times the layout share. For PRs, builds and turnaround, the arm contributes 1%.

### Misses by cell (runs with at least one consumer not updated and live, out of 5)

| change | arm (L1 / L2) | monorepo | multi-repo |
|---|---|---|---|
| C2 rename | A1 open / none | 0 | 0 |
| | A2 structured / partial | 0 | 0 |
| | A3 structured / complete | 0 | 0 |
| | A4 structured / decoy | 0 | 0 |
| | A5 open / catalog | 0 | 0 |
| | A6 open / stale catalog | 0 | 0 |
| | A7 structured + checks / partial | 0 | **2** |
| C3 policy | A1 open / none | 0 | 0 |
| | A2 structured / partial | 0 | **4** |
| | A3 structured / complete | 0 | 0 |
| | A4 structured / decoy | 0 | **5** |
| | A5 open / catalog | 0 | 0 |
| | A6 open / stale catalog | 0 | 0 |
| | A7 structured + checks / partial | 0 | **5** |

C1 (additive, one consumer): 0 misses in all 20 runs; multi-repo took 2 PRs and 8 builds against 1 and 4 (turnaround 91 s against 67 s).

The rename (C2) was almost never missed even with a partial list, because the old name is easy to find (agents searched for `billingUrl` across the repos they had). The policy change (C3) was missed because finding the affected apps means asking "who calls `validateApp`?", and the agents answered from the ticket.

### Scorecard against the predictions recorded before data

| # | Prediction | Result |
|---|---|---|
| 1 | Misses depend on L2 far more in multi-repo; near zero effect in the monorepo | **Supported.** Monorepo 0 of 80; multi-repo 16 of 80, all in structured arms that omit the consumer. Not the shape predicted, though: "none" was safe, "partial" was not |
| 2 | A complete list or catalog removes most of the multi-repo miss gap; a **stale catalog brings misses back** | **First half supported, second half not.** Complete list 0/10, catalog 0/10. Stale catalog **0/10**: the agents used `st deps` (30 queries across the 20 multi-repo A5/A6 runs) but still cloned all five repositories (A5 and A6 averaged 4.8 to 5.0 clones). The open-ended ticket made them explore regardless |
| 3 | A decoy list costs more than no list (wrong work, and the hidden consumer still missed) | **Partly.** Hidden consumer missed (C3 5/5, versus 0/5 for no list). Cost: +23% tokens in multi-repo C2, +51% in monorepo C3, both intervals exclude zero. **No wrong work:** none of the 20 decoy-arm runs opened a PR on the decoy repository |
| 4 | Layout still dominates PR count, builds and lead time | **Supported** (87%, 87%, 60% of variance) |
| 5 | Structured per-repository tasks cut multi-repo exploration and do little in the monorepo | **Supported for exploration, with a cost.** Clones 5.0 to 3.4 in the C3 partial arms; no time saved among correct runs. The saved exploration is the same thing that caused the misses |
| 6 | Acceptance checks reduce rework more than breakdown does | **Not testable.** There were **zero CI failures in 176 runs**, so rework had nothing to measure (90% of its variance is noise). Checks attached to the listed repos made misses worse (A7 7/10 against A2 4/10 and A4 5/10), because a check only covers what is named |
| 7 | A handoff template reduces version-class mismatches in team runs | **Not run** |
| 8 | The policy change shows the largest process effect | **Supported** for misses (multi-repo 0.40 against 0.06 for the rename) |

**Starting positions.** Position B (layout dominates deterministic measures) holds for PRs, builds and lead time. Position A (process explains as much or more of the *misses*) holds for misses in the multi-repo. As the prereg expected, both are partly right, and the split is by outcome.

### Practice ranking under the pre-registered rule

The rule: at least 20% better than the open-ended baseline, interval excluding zero, and the same on the second model.

* **Nothing qualifies as "recommended".** The open-ended baseline already had zero misses, so no practice could improve misses. On lead time, the catalog arms (A5, A6) were faster than the baseline on the policy change among correct multi-repo runs (115 s and 146 s against 161 s median; intervals [-96, -24] and [-80, -6]) and cost fewer tokens (320k and 329k against 379k), but not on the rename (131 s against 131 s), and the second-model subset (one run per cell) cannot confirm it. Treat it as a lead for the next study.
* **Harmful, with the interval excluding zero:** the structured, incomplete-list tickets (A2, A4, A7) on the policy change in the multi-repo layout. The harm check in the prereg exists for exactly this.
* **"RULE MET" lines for turnaround and PR count on those same arms are artifacts.** The runs were faster and used 3 PRs instead of 4 *because they skipped the reports app*. The analysis therefore also reports speed over correct runs only.

### Second model (smaller model, one run per cell)

15 of 16 runs passed. The one miss was **C3, decoy list, multi-repo**, the same cell where Sonnet missed 5 of 5. The smaller model used 2 to 3 times the tokens on several cells and one multi-repo run stalled for 18 minutes before finishing (a latency outlier; kept, and it is why that cell's turnaround is 1,376 s). Too few runs to say more than "the miss reproduced".

### Deviations and choices made after seeing data

* The prereg's 20% rule cannot flag a rise from a zero baseline, so I added **Fisher exact tests** on the miss counts. Added after seeing the miss table.
* I added **correct-runs-only** speed tables after noticing that the fast structured arms were fast because work was skipped. Also after seeing data.
* Everything else in the analysis was fixed beforehand (bootstrap intervals, variance shares, the 20% rule). The tests were not corrected for the number of comparisons: read single p-values near 0.05 (A2, p = 0.048) as suggestive.
* Hidden consumer was always `reports`, and the new app is the one with the least conspicuous name. A different hidden app might show a different size of effect.

### Limits

* Agents, not people. A person given a structured ticket might well ask "who else uses this?"; a person would also face meetings and approvals. The finding is about what a capable agent does when handed a scoped ticket.
* The same model family wrote the tests and played the developers. The scorer detected 17 misses (16 Sonnet, 1 smaller model); two of them were verified by hand against the agents' own reports, and against the unmodified baseline, which it fails on every change-specific check.
* A toy system: three consumers, one shared contract, no merge conflicts, no flaky CI. Zero CI failures means this study says nothing about rework.
* Tickets come from templates, cleaner than real ones. Real tickets are noisier and less often "structured with a wrong scope" than "unstructured with a vague scope".
* Five replicates per cell, one per cell for the second model. The big contrasts (0/20 against 14/15) are not close calls, but the small ones (token costs, catalog speed) are.
* Timings are good only because a background loop kept the Docker VM clock in step; it logged 83 corrections of about 300 s during the runs. Largest boundary skew was 1 s.

### Not done, and what comes next

* **Not run:** work breakdown into epics (L3), clarification (L4; `st ask` and the scripted requester are built and unused), team handoff (L5), review input (L6). The first question each leaves open is below.
* **The result worth following up:** does the structured-ticket miss go away if the ticket says "list every consumer yourself" or if the acceptance criterion is made executable (a check that fails when any app still has the old behavior)? Tickets (A7) that attached checks per listed repo made it worse; a global check was never tried.
* Vary which consumer is hidden, and add a fourth change type where one consumer is genuinely unaffected, to see whether the open-ended "explore everything" habit costs time when most repos are irrelevant.
* Try a more realistic estate: dozens of repositories, where "clone everything" stops being the cheap default. The open-ended arms may stop being safe.
* Fold in the survey's still-open suggestions ([the outside-sources survey](outside-sources.md)): a wrong-implementation-hint level, a solution-leakage control, noisy tickets.

**Pre-registration status.** [the pre-registration](pre-registration.md) was never locked before running (the survey and a 12-run pilot were replaced by the survey and one pilot round); this note records exactly what ran in its place.

---

# Phase 2: can the structured-ticket miss be fixed, and does it generalise?

**Pre-registered 2026-10-30 before the first phase-2 round (launched 13:25).** Same field, same harness, same model (Sonnet), same scorer. Only the policy change (C3) is used, because it is where the phase-1 effect lived. Both layouts run in every round, as before. Controls are the phase-1 cells (5 replicates each, same harness): A1 open, A2 structured/partial, A3 structured/complete, A5 catalog.

## Arms

| Arm | Ticket (all structured per repository, listing billing and shell; reports hidden, unless stated) | What it tests |
|---|---|---|
| **B1 discover** | A2 plus one line: "Before you start, find every app that uses `validateApp` (not only those below) and add a sub-task for each with `st task add`." | An instruction to look, with no extra information |
| **B2 audit** | A2 plus an acceptance line "`st audit` reports no violations" and an `st audit` command that scans the main branch of every app repository for `validateApp` calls without an `owner` | A global, executable acceptance check (what the phase-1 A7 checks were not: those covered only listed repos) |
| **B3 ask** | A2 plus `st ask` (up to 3 questions, scripted neutral answers that never name consumers) | Whether the option to clarify gets used and helps |
| **B4 caveat** | A2 plus one line in the description: "The sub-tasks below cover the apps we know about. Others may also be affected." | An honest incompleteness warning |
| **A2s** | A2, but the hidden consumer is **core-shell** (list names billing and reports) | Whether the miss is about `reports` or about an unlisted consumer |

5 replicates per arm = 25 rounds (50 runs), shuffled, replicate-major.

## Predictions (recorded before data)

1. **B1** cuts multi-repo misses to at most 1 of 5 (agents follow explicit instructions).
2. **B4** helps less than B1: 2 or 3 of 5 still miss.
3. **B2** is the most reliable fix, at most 1 of 5 missing, **provided the agent runs `st audit`**; we will report how many ran it.
4. **B3** does not help: 3 or more of 5 still miss, because agents rarely ask when they believe the ticket is complete.
5. **A2s** misses at least 3 of 5 (the effect is about being unlisted, not about `reports`).
6. The monorepo has 0 misses in every arm.
7. B1, B2 and B4 add little cost: tokens within 20% of A2 among correct runs.

A practice is called a fix if misses fall from phase-1 A2 (4 of 5) to at most 1 of 5 with Fisher p below 0.05; with n = 5 per cell, anything weaker is reported as a lead.

## Phase 2 results (50 runs, 25 rounds, run 13:25 to 14:49)

All valid, none excluded. Controls are the phase-1 cells (run earlier, same harness; not concurrent, so a drift in the model or machine between the two would show up as a difference this design cannot separate). Full tables: `analysis-phase2.md` in `data/README.md` (outside the notes tree; see where the bulk data lives).

| Arm (multi-repo, C3, n = 5 each) | Runs with a missed consumer | Opened the hidden repo | Other behaviour | Fisher p vs A2 (partial list) |
|---|---|---|---|---|
| A2 partial list (phase 1) | **4/5** | 2/5 | | n/a |
| A1 open-ended (phase 1) | 0/5 | 5/5 | | 0.048 |
| **B1** "find every app that uses `validateApp`" | **0/5** | 5/5 | recorded 1.0 sub-tasks on average | 0.048 |
| **B2** global `st audit` acceptance check | **0/5** | 5/5 | ran the audit in 5/5, every final report clean | 0.048 |
| **B3** `st ask` available | **4/5** | 4/5 | **asked 0 questions in 25 runs** | 1.000 |
| **B4** "others may also be affected" | **0/5** | 5/5 | | 0.048 |
| **A2s** same partial list, hidden app is core-shell | **2/5** | 3/5 | | 0.52 |

Monorepo: 0 misses in all 25 runs again, and 0 of 105 across both phases.

### What it means

1. **The miss is cheap to fix, and the fix is wording.** One added sentence ("others may also be affected"), one added instruction ("find every app that uses it"), or an executable organisation-wide check each took misses from 4 of 5 to 0 of 5. That is the structured ticket's benefit kept (a scoped plan, no wasted exploration) without its cost. Two of the fixes did not make the work slower or more expensive among correct runs: B1 took 136 s and 302k tokens against 161 s and 379k for the open-ended arm (interval on time [-74, -3]); B4 and B2 were within the open-ended baseline's range.
2. **The audit worked because the agents ran it.** All five B2 agents ran `st audit` and every final report was clean. Agents followed an acceptance line that named a command; the phase-1 acceptance criterion in prose ("every app that calls `validateApp` passes its owning team") was not enough, though it was in the same ticket.
3. **Offering a clarification channel did nothing.** Zero questions in 25 runs, and four of five B3 multi-repo runs still missed. The agents were not uncertain; they believed the ticket's scope.
4. **They knew, and said so, and skipped it anyway.** In all four B3 misses the agent opened the reports repository, noticed it also calls `validateApp` without an owner, and wrote in its summary something like "reports also calls validateApp without owner but was not in the ticket; it stays on ^1.0.0 so it still works". The information was in the report. Whether a human reading that report would catch it is a question about people this study cannot answer. The point for process is that **the ticket's scope was treated as a limit on the job, not as a starting point.**
5. **The hidden app mattered somewhat.** With core-shell hidden the miss rate was 2/5, not statistically different from either the partial-list arm or the open-ended arm. The `reports` result may be partly about `reports`. A fair reading of phase 1 and 2 together is that the effect is real (it reproduced across A2, A4, A7, B3 and the smaller model) but its size depends on the app.

### Scorecard for the phase-2 predictions

| # | Prediction | Result |
|---|---|---|
| 1 | B1 at most 1 of 5 miss | **Right** (0/5) |
| 2 | B4 helps less than B1, 2 or 3 of 5 still miss | **Wrong.** B4 was as good as B1 (0/5). The cheapest change was enough |
| 3 | B2 at most 1 of 5 miss, provided the audit is run | **Right** (0/5; run 5/5) |
| 4 | B3 does not help, 3 or more of 5 miss | **Right** (4/5; 0 questions asked) |
| 5 | A2s misses at least 3 of 5 | **Wrong** (2/5). The effect is weaker with a different hidden app |
| 6 | Monorepo 0 misses everywhere | **Right** (0/25) |
| 7 | B1, B2, B4 add little cost | **Right** against the open-ended baseline (B1 cheaper, B2 +5% tokens, B4 -8%); A2 had only one correct run, so it cannot serve as the comparison |

Under the fix rule fixed before the phase (misses from 4/5 to at most 1/5, p below 0.05): **B1, B2 and B4 qualify**, each at p = 0.048. That p-value is the best a 4-vs-0 split of 5 against 5 can give, and three such comparisons were made, so treat it as a clean directional result, not a strong test.

---

# Phase 3: does "open-ended tickets are safe" survive a larger estate?

**Pre-registered 2026-10-30 before the first phase-3 round (launched 14:51).** Phase 1 found open-ended tickets and catalog arms never missed a consumer in the multi-repo layout, because those agents cloned every repository (5.0 clones) before acting. That is cheap with 5 repositories. This phase asks whether it stays cheap, and safe, with 17.

## Design

Same field plus an **estate** of 12 unrelated repositories (multi-repo: `apps-analytics-dashboard`, `apps-admin-console`, `apps-help-center`, `apps-marketing-site`, `libs-ui-kit`, `libs-logger`, `libs-i18n`, `svc-notifications`, `svc-auth-proxy`, `svc-search`, `svc-export`, `tools-release-notes`; monorepo: the same 12 as directories under `packages/`, outside the MFE pipelines). None uses the shared contract, none has a Jenkins job. The three real consumers and the hidden app (`reports`) are unchanged, so the same scorer applies. `st repos` now lists 17 repositories in the multi-repo layout (the monorepo is still one repository plus the platform kit).

Change C3 only. Six arms, both layouts, 5 replicates each (30 rounds), shuffled replicate-major, Sonnet, tag `s4`: **A1** open, **A2** structured/partial, **A3** structured/complete, **A5** open + catalog (complete), **A6** open + stale catalog, **B4** structured/partial + "others may also be affected". Controls are the phase-1/2 cells at 5 repositories.

## Predictions (recorded before data)

1. **A1** (open): multi-repo misses rise from 0/5 to at least 1/5, and mean clones fall below 12 of the 17 (agents stop exhaustively exploring).
2. **A6** (stale catalog): at least 2/5 miss (the agent trusts the catalog when exploring is expensive). This is prediction 2 of the original study, retested where it may finally apply.
3. **A5** (complete catalog) and **A3** (complete list): 0/5.
4. **A2** (partial list): at least 4/5 miss, as before.
5. **B4** (caveat): at most 1/5 miss, with more clones and tokens than at 5 repositories.
6. Monorepo: 0 misses in every arm; time and tokens within 20% of the 5-repository result.
7. Multi-repo open-ended arms cost at least 20% more tokens than at 5 repositories.

---

# Phase 4: do the fixes hold on a second model?

**Pre-registered 2026-10-30 before the first phase-4 round (launched 16:15).** The original rule for calling a practice "recommended" requires that it also holds on the second model; phases 2 and 3 used only Sonnet. Phase 4 repeats the key contrast with the smaller model (`haiku`) on the original 5-repository field, change C3, both layouts, **4 replicates** per arm (the smaller model is slower and more variable, and four is what the night allows), tag `s5`.

Arms: **A1** open-ended, **A2** structured/partial (the problem), **B1** "find every app" instruction, **B2** global audit, **B4** "others may also be affected". 5 arms x 4 reps = 20 rounds, shuffled replicate-major.

## Predictions (recorded before data)

1. **A2** on the smaller model: at least 3 of 4 multi-repo runs miss the hidden consumer (the problem reproduces).
2. **A1**: at most 1 of 4 misses.
3. **B1, B2, B4**: each at most 1 of 4 misses. The smaller model follows explicit instructions less reliably, so I expect B1 and B4 to be the weaker ones, B2 (a command to run) the stronger.
4. **Monorepo**: 0 misses in every arm.
5. The smaller model costs at least 1.5 times the Sonnet tokens in every arm (as in the earlier subset).

A practice is "recommended" under the original rule only if, on both models, misses fall at least 20% from A2 with the interval excluding zero. With n = 4 on this model, the achievable best is 0 of 4 against 4 of 4 (Fisher p = 0.029); anything between is reported as a lead.

## Phase 3 results (60 runs, 30 rounds, run 14:51 to 16:15)

None excluded. Controls are the same arms at 5 repositories from phases 1 and 2 (not concurrent). Full tables: `analysis-phase3.md` in the data folder.

| Arm (C3) | multi-repo misses at 5 repos | at 17 repos | repos cloned at 5 -> 17 (of 5 / 17) | cloned the hidden repo at 17 |
|---|---|---|---|---|
| A1 open-ended | 0/5 | **0/5** | 5.0 -> **15.4** | 5/5 |
| A2 structured / partial | 4/5 | **5/5** | 3.4 -> 3.8 | 4/5 |
| A3 structured / complete | 0/5 | 0/5 | 4.0 -> 4.0 | 5/5 |
| A5 open + catalog | 0/5 | 0/5 | 5.0 -> 11.6 | 5/5 |
| A6 open + **stale** catalog | 0/5 | **0/5** | 4.8 -> 10.8 | 5/5 |
| B4 partial + "others may be affected" | 0/5 | 0/5 | 4.2 -> 5.6 | 5/5 |

Monorepo: 0 misses in all 30 runs again (0 of 135 Sonnet monorepo runs across the study so far).

### What it means

1. **Open-ended tickets stayed safe at 17 repositories.** The agents did not stop exploring: four of five A1 runs cloned all 17 (the fifth cloned 9) and all found the hidden app. The "clone everything" habit did not weaken within this range. What happens at 100 or 1,000 repositories is not answered here, and I would not extrapolate from 17: cloning everything stops being something an agent (or a person) would do.
2. **The stale catalog still did not mislead.** The catalog arms used it (1 or 2 `st deps` queries per run) and cloned fewer repositories than the open-ended arm (11.6 and 10.8 against 15.4), but all ten found the hidden app anyway, including one run that cloned only 4 repositories. In every run the agent treated the catalog as a hint to check, not as the answer. Prediction 2 of the original study (a stale catalog brings misses back) failed again.
3. **The structured-partial miss got slightly worse, not better.** 5 of 5 missed at 17 repositories (4 of 5 at 5). Four of the five *opened* the reports repository and still left it out, which is the scope-following mechanism again, now more common than the "did not look" cause.
4. **The caveat sentence still worked** (0/5) at the cost of more exploration (4.2 to 5.6 repositories) and about 8% more tokens.
5. **Cost of the larger estate was small.** Multi-repo tokens moved between -23% and +16% by arm, turnaround between -16% and +8%, with no interval that is clearly away from zero except A1 multi getting *faster* (161 to 135 s, [-72, -8]), which is more likely run-to-run and phase-to-phase variation (the controls were run hours earlier) than an effect of having more repositories. One monorepo cell (A1) rose 28% in tokens (242k to 310k) without a change in outcome.

### Scorecard for the phase-3 predictions

| # | Prediction | Result |
|---|---|---|
| 1 | A1 misses rise to at least 1/5 and clones fall below 12 of 17 | **Wrong on both.** 0/5 misses; 15.4 of 17 cloned |
| 2 | A6 (stale catalog) at least 2/5 miss | **Wrong.** 0/5 |
| 3 | A5 and A3 stay 0/5 | **Right** |
| 4 | A2 at least 4/5 miss | **Right** (5/5) |
| 5 | B4 at most 1/5 miss, more clones and tokens | **Right** (0/5; clones +1.4, tokens +8%) |
| 6 | Monorepo 0 misses; time and tokens within 20% of the 5-repo result | **Half right.** 0 misses; turnaround within 20% in all arms but B4 (+22%, 63 to 77 s), tokens within 20% in all arms but A1 (+28%) |
| 7 | Multi-repo open-ended arms cost at least 20% more tokens | **Wrong.** A1 was 23% cheaper; A5 +16%, A6 +11% |

Three of the seven predictions were wrong, and the wrong ones share a cause: I assumed the agents' exploration would be cost-limited. In this setup it was not. They were limited by what they believed their job was.

**Limit of this phase.** The 12 added repositories are small, unrelated and obviously irrelevant by name. A real estate has repositories that look related, call similarly named functions, or consume the contract under a different name. This phase tests the number of repositories, not their ambiguity.

## Phase 4 results (40 runs, 20 rounds, smaller model, run 16:15 to 18:11)

One round (B1, replicate 3) was killed by the 25-minute cap when the agent stalled mid-run; it was set aside and re-run, and the re-run is the one counted. An earlier smaller-model run stalled for 18 minutes and then finished. Both look like model or API latency, not treatment effects, but a stalled-then-retried run is a selection I cannot rule out as harmless. Full table: `analysis-phase4.md` in the data folder.

| Arm (C3) | Smaller model, multi-repo misses | Fisher p vs its own A2 | Opened hidden repo | Sonnet, same arm | Tokens vs Sonnet |
|---|---|---|---|---|---|
| A1 open-ended | 0/4 | 0.029 | 4/4 | 0/5 | 2.8x |
| **A2 structured / partial** | **4/4** | - | **0/4** | 4/5 | 2.4x |
| **B1** "find every app" | **0/4** | 0.029 | 4/4 | 0/5 | 2.8x |
| **B2** global audit | **1/4** | 0.143 | 3/4 | 0/5 | 2.4x |
| **B4** "others may be affected" | **0/4** | 0.029 | 4/4 | 0/5 | 3.4x |

Monorepo: 0 misses in all 20 runs (0 of 163 monorepo runs across the study).

* **The problem reproduces more sharply on the smaller model:** with a partial list it *never opened* the hidden repository (0/4; Sonnet opened it in 2/5 and then skipped it), and missed it every time.
* **B1 and B4 hold on the second model**, each 0/4 against 4/4.
* **B2 was the weakest fix on the smaller model, not the strongest** (my prediction had it the other way round). The miss is instructive: the agent ran `st audit` twice, saw one violation, wrote in its final report "OPEN: st audit still reports 1 violation for sub-route-reports (never in ticket scope)... acceptance criterion 'audit reports no violations' is therefore NOT fully met", and closed the ticket anyway. An executable check made the gap visible and honest in the report; it did not make the agent act on it. In a process with a human reviewer the report is a catch; in one without, the check was advisory.
* **The smaller model used 2.4 to 4.7 times the tokens** for the same outcomes.

| # | Prediction | Result |
|---|---|---|
| 1 | A2: at least 3 of 4 multi-repo runs miss | **Right** (4/4) |
| 2 | A1: at most 1 of 4 misses | **Right** (0/4) |
| 3 | B1, B2, B4 each at most 1 of 4; B2 strongest, B1 and B4 weaker | **Counts right, ranking wrong.** B1 0/4, B4 0/4, B2 1/4 |
| 4 | Monorepo 0 misses | **Right** (0/20) |
| 5 | At least 1.5x the Sonnet tokens in every arm | **Right** (2.4x to 4.7x) |

---

# State of the study after four phases

326 valid runs, no run excluded for harness reasons after the 07:51 restart (one run timed out and was re-run, one overnight round was voided and re-run). All counts are exact; the effects that are strong are strong in raw counts, not through modelling.

## Practice ranking under the pre-registered rule

The rule: at least 20% better than the baseline with the interval excluding zero, **on both models**.

| Practice | Sonnet | Smaller model | Verdict |
|---|---|---|---|
| **B4: add "the sub-tasks below cover the apps we know about. Others may also be affected."** | 0/5 vs 4/5 (p = 0.048); held at 17 repositories, 0/5 | 0/4 vs 4/4 (p = 0.029) | **Recommended** |
| **B1: tell the developer to find every app that uses the changed thing and add a sub-task for each** | 0/5 vs 4/5 (p = 0.048) | 0/4 vs 4/4 (p = 0.029) | **Recommended** |
| B2: org-wide executable acceptance check | 0/5 vs 4/5 (p = 0.048) | 1/4 vs 4/4 (p = 0.143) | Not recommended on its own: the failing check was reported and overridden |
| B3: let the developer ask clarifying questions | 4/5 (no better) | not run | **No effect**; no questions were asked in 25 runs |
| A5/A6: dependency catalog, complete or stale | 0/10 misses | not run | Safe either way here, but only because the agents also explored (cloned 4 to 17 repos at 17-repo scale); a faster-than-baseline signal on the policy change (115 s and 146 s against 161 s) is a lead only |
| A7: acceptance checks attached to the listed repos only | worse, pooled over C2 and C3 (7/10 miss vs 4/10 for A2) | not run | **Harmful**: checks cover only what is named |
| Structured per-repository ticket that omits a consumer (A2, A4) | 9/10 miss | A2 4/4 | **Harmful** in multi-repo; no effect in the monorepo |

## What I think the study shows, in plain terms

1. **Layout decides how many PRs, builds and minutes a crossing change takes, and the ticket cannot change that.** The monorepo was 1 PR and 4 builds, the multi-repo 3 to 4 PRs and 12 to 16 builds, in every ticket variant tested.
2. **The ticket decides whether a crossing change is complete, but only in the multi-repo layout.** In the monorepo, 163 of 163 runs were complete, whatever the ticket said: the agent searched one tree. In the multi-repo, a scoped ticket became a limit on the job. The same agents given an open-ended ticket explored everything and were complete.
3. **The fix is a sentence, not a process.** "Others may also be affected" or "find every app that uses this" restored completeness on two models with no measurable cost. That contradicts the folk wisdom in either direction: more structure was not better, and less structure was not necessary. What mattered was whether the ticket told the developer that its list was not the whole job.
4. **The scope of a ticket was obeyed even when the developer knew better.** Of the 33 multi-repo misses across all phases, 12 had opened the hidden repository, and the final summary of each of those 12 mentions the hidden app in terms of scope (a keyword match on the summary, not 12 individual readings; I read about six by hand, including the audit-arm miss). The other 21 never opened it. Whether a person would act on a note like that is the part of the process this study cannot see.
5. **Dependency catalogs, even stale ones, did no harm here.** Agents used them as hints.

## Limits that matter most

* Agents are not people. A reviewer reading "reports also calls validateApp without owner, left alone" may well act on it, and that would change the practical cost of the miss.
* One hidden app mostly (`reports`); with a different hidden app (core-shell) the effect was 2/5, not significantly different from the controls.
* Phases 2 to 4 compare against phase-1 controls run hours earlier, not concurrently.
* The estate in phase 3 had unrelated, obviously irrelevant repositories. Ambiguous ones would be a harder test.
* Five replicates (four on the smaller model) per cell. The headline contrasts (0/5 against 4/5, 14/15 against 0/20) are large. Cost differences of 10 to 20% are not resolved.
* Most important: **zero CI failures** in all 326 runs. Rework, flaky pipelines and merge conflicts were never exercised.

## Still not run

Work breakdown into epics (L3), clarification beyond the one-arm test (L4), team handoff between two developers (L5, where the first study saw the version-class mismatch caught), review input (L6, the reviewer side of "diff plus consumer list"), a fourth change type with a genuinely unaffected consumer, noisy tickets, and repositories that look related but are not. L5 and L6 are the ones I would do next: they are where a human or a second agent sits between the ticket and "done".

---

# Phase 5: can a reviewer catch the app the developer left out? (review input, L6)

**Pre-registered 2026-10-30 before the first review ran.** Phases 1 to 4 showed a developer given a scoped ticket often leaves an affected app alone, and often says so in its closing note. This phase asks what a second agent, reviewing the change before it is accepted, catches. Reviews do not use the field; they run on the saved results of phases 1 to 4.

## Cases (ground truth known from the live-bundle scorer)

All multi-repo policy-change (C3) runs from phases 1 to 4 where the developer ran without an API error: **30 incomplete** (an app left unfixed; 25 by the main model, 5 by the smaller model; hidden app `reports` in 28, core-shell in 2) and **30 complete**, drawn at random (seed fixed) from the 80 complete ones. Each case is the ticket as the developer saw it, the combined diff of everything it merged (lockfiles excluded), and, in one arm, the developer's closing summary. Cases are shuffled and carry opaque ids. Monorepo cases are not used: there was never an incomplete one to catch.

## Arms (the same 60 cases in every arm, so arms are compared case by case)

| Arm | The reviewer sees | Can look at the repositories? |
|---|---|---|
| **V0** | ticket and diff | No (no tools at all) |
| **V1** | ticket and diff | Yes, read-only, as they were before the change (Read, Glob, Grep) |
| **V2** | ticket and diff, plus the checklist line "if the change alters something shared, check that every app which uses it was updated" | Yes, same as V1 |
| **V3** | ticket and diff, plus the true list of apps that use the shared contract | No |
| **V4** | ticket and diff, plus the developer's closing summary (as a PR description would carry) | No |

The reviewer answers with a verdict (approve or request changes) and a list of issues, in a fixed JSON form. A review **catches** an incomplete case if the verdict is "request changes" and an issue names the missing app (by script, using the app's repository and directory names). A review **raises a false alarm** if it requests changes on a complete case. Sonnet is the reviewer in every arm. One review per case per arm: 300 reviews.

## Predictions (recorded before data)

1. **V0** catches at most 20% of the incomplete cases (what is missing is not in the diff).
2. **V1** catches between 30% and 70%: the reviewer can look, but has no reason to.
3. **V2** and **V3** each catch at least 80%.
4. **V4** catches at least 40% overall, and nearly all of the cases in which the developer's summary names the missing app and almost none of the others.
5. False alarms on complete cases stay at or below 20% in every arm.
6. V1 and V2 cost at least 2 times the tokens of V0.
7. The catch rate does not depend on which model was the developer, within the sample.

## Phase 5 results (300 reviews, 60 cases, run 20:58 to 21:09)

All 300 reviews usable (three were unparsable on the first pass and were re-run once; the re-run is the one counted). Same 60 cases in every arm. Full tables, including the paired tests and a sample of false-alarm text: `analysis-phase5.md` and `review/` in the data folder.

| Arm: the reviewer sees | Named the missing app and asked for changes (of 30 incomplete) | Asked for changes, any reason | Approved an incomplete change | False alarms (of 30 complete) | Tokens |
|---|---|---|---|---|---|
| **V0** ticket + diff | **0/30** | 5/30 | 25 | 2/30 | 6k |
| **V1** + can look at the repos | **27/30** (90%) | 27/30 | 3 | 0/30 | 38k |
| **V2** + checklist line, can look | **29/30** (97%) | 29/30 | 1 | 0/30 | 32k |
| **V3** + the true list of apps | **25/30** (83%) | 30/30 | 0 | 0/30 | 6k |
| **V4** + the developer's summary | **11/30** (37%) | 12/30 | 18 | 6/30 | 6k |

Each of V1 to V4 caught cases V0 never did and lost none: 27, 29, 25 and 11 paired cases, p below 0.0001 for the first three, 0.001 for V4.

### What it means

1. **The diff alone cannot show what is missing.** A reviewer who sees only the change caught 0 of 30. An approving verdict on the 25 of them says nothing was wrong with what was present; the omission is outside the diff.
2. **A reviewer who is allowed to look, catches it, without being told to.** With read access to the repositories and no hint at all (V1), 27 of 30 incomplete changes were caught, against my prediction of 30 to 70%. The ticket itself says "every app that calls `validateApp`", and a reviewer who can search takes that at its word, where the developer, with the same words and the same access, often did not. The checklist line (V2) added two more.
3. **Giving the reviewer the true list also works (V3), but with a twist.** The verdict was "request changes" in all 30 cases, yet in 5 of them the reviewer named the wrong problem. All five were decoy-list tickets: the reviewer flagged the platform-kit sub-task, which the ticket asked for and nobody did, and never noticed that reports, on the list it had been handed, was missing from the diff. The same five gave V0 a right verdict for the wrong reason. A wrong list in the ticket can be enough to occupy a reviewer.
4. **The developer's own note is a weak channel (V4).** In 24 of the 30 incomplete cases the developer's summary said the missing app had been left alone (usually "it stays on ^1.0.0 so it is unaffected"). Given that sentence, the reviewer asked for changes in 11 of the 24 and approved in 12 (one more asked for changes for another reason). When the summary did not mention the app, the reviewer caught 0 of 6. So **the omission was disclosed, and the disclosure was accepted about half the time.** The reviewer also had the most false alarms in this arm (6 of 30, mostly "what about platform-kit?").
5. **Cost.** Reviews with repository access cost 5 to 6 times the tokens of a diff-only review (38k and 32k against 6k), about two cents a review.

### Scorecard for the phase-5 predictions

| # | Prediction | Result |
|---|---|---|
| 1 | V0 catches at most 20% | **Right** (0%) |
| 2 | V1 catches 30% to 70% | **Wrong.** 90% |
| 3 | V2 and V3 each catch at least 80% | **Right** (97%, 83%; V3 is 100% on verdict) |
| 4 | V4 catches at least 40% overall, nearly all where the summary names the app and almost none otherwise | **Mostly wrong.** 37% overall; 11 of 24 where the summary named it (not "nearly all"); 0 of 6 otherwise (right) |
| 5 | False alarms at most 20% in every arm | **Right, just** (V4 was exactly 6 of 30) |
| 6 | V1 and V2 cost at least twice V0's tokens | **Right** (about 5 to 6 times) |
| 7 | Catch rate does not depend on the developer model | **Cannot tell.** 5 incomplete cases came from the smaller model; V1 caught 5 of 5, V4 1 of 5 |

### Limits specific to this phase

* The reviewers are Sonnet agents, one review per case per arm. The 60 cases are not independent draws: several share an arm and a ticket text, and the 30 complete ones were sampled from 80.
* Complete cases are mostly easy ones (they were complete because the developer searched widely), and 5 of the 30 incomplete are the decoy-list tickets that confuse reviewers.
* The "named the app" test is a keyword match on the issue text (checked by hand for the 5 V3 wrong-reason cases).
* A reviewer here sees the whole change set at once. In practice each repository's PR is reviewed separately, often by someone who sees only that repository's diff, which is the V0 condition.
* The V1 and V2 reviewers had read tools and were told to stay in the repository folder. The saved output does not record their tool calls, so I cannot show that none of them read outside it (for example the results folder, which holds the ground truth). I did not check.

---

# Phase 6: two developers on one ticket; does a handoff help? (L5)

**Pre-registered 2026-10-30 before the tooling for this phase was built and before any run.** In the first study two developers splitting a ticket helped only on independent tasks, and a message between them caught a minor-versus-major release mismatch. This phase isolates the handoff.

## Design

The policy change (C3), the original 5-repository field, **both layouts**, the ticket with the **complete** list of apps (arm A3), so a missing app cannot come from the ticket. The ticket is split between two developers on the board:

* **dev-a:** the contract change and the billing app.
* **dev-b:** the core-shell app and the reports app.

dev-b's two tasks depend on dev-a's release of the contract. The two developers are separate agents working at the same time; they share only the board, the PR list, the CI and CD results, and whatever the condition lets them send each other. Three conditions, 5 replicates each:

| Condition | What the developers have |
|---|---|
| **H0 no channel** | the shared board and PR list only; `st msg` and `st handoff` do not exist |
| **H1 free messages** | `st msg send/inbox/wait` as in the first study |
| **H2 required handoff** | no free messages; instead, when a developer releases something others depend on, the brief requires a handoff note (released version, release class, what changed, who must act) with `st handoff post`, which the other developer reads with `st handoff show` |

Each round runs the monorepo pair and the multi-repo pair at the same time (four agents). Scored by script on the live bundles, as before: a run is **complete** if all three apps run with the new behaviour. Also recorded: PRs, merge conflicts, CI failures, PR updates, the time dev-b waits, messages and handoffs, makespan, tokens and cost. 15 rounds (30 runs), tag `s6`.

## Predictions (recorded before data)

1. Multi-repo **H0** has more incomplete runs than H1 or H2: at least 2 of 5 incomplete in H0 and at most 1 of 5 in each of H1 and H2. (The failure to expect is dev-b adopting a range that never resolves the new major version.)
2. **H2** has fewer release-class or version mismatches than **H1**, and more consistent information per handoff, but no better completeness (both near 5 of 5).
3. dev-b's total waiting time is longest in H0.
4. The monorepo has 5 of 5 complete in every condition, and more merge conflicts than the multi-repo.
5. Two developers are not faster than the one-developer arm A3 on the same change (median single-developer multi-repo turnaround 148 s): the median multi-repo team makespan is at least 0.8 times that, in every condition.
6. H1 produces at least 3 free messages per run on average.

## Phase 6 results (30 runs, 15 rounds, run 21:41 to 22:23)

All 30 runs complete in both layouts and all three conditions; no timeouts, no merge conflicts, no CI failures, no PR updates in the multi-repo runs. Full table: `analysis-phase6.md` in the data folder.

| Condition (5 runs each) | Multi-repo complete | Monorepo complete | Multi-repo makespan, median | Free messages (multi / mono, mean) | Handoff notes posted / read (multi) |
|---|---|---|---|---|---|
| H0 no channel | 5/5 | 5/5 | 106 s | 0 | n/a |
| H1 free messages | 5/5 | 5/5 | 99 s | 1.6 / 2.6 | n/a |
| H2 required handoff note | 5/5 | 5/5 | 98 s | n/a | 5 / 34 |

**The handoff made no measurable difference on this change.** In the no-channel condition dev-b's closing reports say how: it edited its two apps while dev-a's contract PR was in flight, then polled the PR list and the registry until `@mfe/shared-contracts` 2.0.0 appeared, then updated its dependency. "I never messaged dev-a; the board and the registry were enough." The team's release rules make a breaking change's version predictable (major), so the registry carried the handoff. One H0 multi-repo run was an outlier: dev-b's app merged at 589 s against about 60 s in the other 14 multi-repo runs, which I did not investigate. The monorepo needed less coordination still: dev-b's PRs merged before dev-a's contract PR in most runs (the old `validateApp` ignores an extra `owner`).

Two developers were faster than one on this change (multi-repo median 98 to 106 s against 148 s for one developer on the same ticket, phase 1 A3), at 1.6 to 1.9 times the tokens, because the two halves ran at the same time after the contract was live.

### Scorecard for the phase-6 predictions

| # | Prediction | Result |
|---|---|---|
| 1 | H0 has at least 2/5 incomplete; H1 and H2 at most 1/5 | **Wrong.** 0/5 incomplete everywhere |
| 2 | H2 has fewer release-class mismatches than H1 | **No mismatch anywhere** |
| 3 | dev-b waits longest in H0 | **Not measurable as stated:** the wait is only recorded for the message channel; dev-b's finish time was 89 to 106 s in 4 of 5 H0 runs and 611 s in the fifth |
| 4 | Monorepo 5/5 complete with more merge conflicts than multi | **Half right.** 5/5 complete; no merge conflicts in either layout |
| 5 | Two developers are no faster than one (at least 0.8 times the single-developer median) | **Wrong.** 0.66 to 0.72 times |
| 6 | H1 averages at least 3 free messages per run | **Wrong.** 1.6 (multi) and 2.6 (mono) |

**Why a null result is not the end of the question.** The release class here was not in doubt, so there was nothing for the developers to disagree about. The first study saw a message matter when it was (a minor-versus-major call on a change to a returned string). Phase 7 builds that case.

**One harness fix before the data (phase 6).** Two merges to the same repository in quick succession left the first merge's commit without its own main build (Jenkins builds only the latest), so the first developer's `deploy wait` timed out. Deploy-wait now accepts a later build that contains the merge. It was found in a test round and fixed before any counted run.

---

# Phase 7: a release whose class is a judgement call (L5 again)

**Pre-registered 2026-10-30 before the tooling for it was built and before any phase-7 run.**

## Design

Same two-developer split, same three conditions (H0 no channel, H1 free messages, H2 required handoff note), both layouts, 5 replicates, complete list, tag `s7`. The change changes:

**C4: the billing service has moved to a versioned path.** In the shared configuration, change the **value** of `billingUrl` from `https://homelab.local/billing` to `https://homelab.local/billing/v2` (same name, new value); every app should end up using the new address. The ticket says to release it following the team's rules (breaking is major, additive is minor, fix is patch) and does not say which this is: a value change to an existing field is a defensible patch, minor or major. dev-a owns the contract release and billing; dev-b owns shell and reports and must adopt whatever dev-a releases. A run is **complete** if all three live bundles carry the new address.

## Predictions (recorded before data)

1. **The class varies.** Across the 15 multi-repo runs, dev-a chooses at least two different release classes.
2. **H0:** at least 2 of 5 multi-repo runs are incomplete or have dev-b finishing more than 300 s after the start (it waits for or installs a version it guessed wrongly).
3. **H1 and H2:** at most 1 of 5 each.
4. In H2 the version and class in the posted note match the registry in 5 of 5 runs.
5. The monorepo is 5/5 complete in H0 and H1 and H2 together except for runs affected by the shipped CD blind spot (a change in `libs/` alone deploys nothing); any monorepo failure will be reported with its cause.

## Phase 7 results (30 runs, 15 rounds, run 22:25 to 23:31)

None excluded. All 30 runs were complete eventually. Full table: `analysis-phase7.md`.

| Condition (5 multi-repo runs each) | Complete | Release class chosen by dev-a (major / minor / patch) | dev-b finished after 300 s | dev-b finish time, seconds | Makespan, median |
|---|---|---|---|---|---|
| **H0** no channel | 5/5 | 1 / 3 / 1 | **4/5** | 100, 464, 478, 683, 690 | **478 s** |
| **H1** free messages | 5/5 | 2 / 3 / 0 | 0/5 | 86 to 99 | 97 s |
| **H2** required handoff note | 5/5 | 3 / 1 / 1 | 0/5 | 85 to 116 | 106 s |

Monorepo: 5/5 complete in each condition, makespan 91 to 95 s, no conflicts. All 15 monorepo runs edited each app's `package.json` (a version bump or similar) so that CD would rebuild it, which works around the shipped pipeline's blind spot (a change in `libs/` alone deploys nothing); none hit it.

* **The class really was a judgement call:** across the 15 multi-repo runs dev-a released 6 major, 7 minor and 2 patch.
* **No channel cost time, not correctness.** With no channel, dev-b was slow in 4 of 5 runs (464 to 690 s against about 100 s in the other 10; Fisher p = 0.004 for H0 against the other two together, 0.048 against H1 alone). Every one of them finished correctly: the registry always told them in the end.
* **The cost was the waiting loop.** The reports of the slow dev-b agents say why. Two waited for the board to show dev-a's task as done, but dev-a did not mark it until the end (the board "still showed task 1 as `todo` after PR #1 had merged and deployed"). One's polling loop "looked for 1.1 or 2.0, so it missed 1.0.1 and ran the full 10 minutes, even though 1.0.1 was already there". One hit the 10-minute command limit. With messages or a handoff note the dependent developer learned the exact version and class and had its apps merged 24 to 37 s after the contract was live.
* **The handoff notes were right every time:** the version and class in the posted note matched what the registry held in 5 of 5 runs (2.0.0 major three times, 1.1.0 minor, 1.0.1 patch). The dependent developer read the note 37 times across the five H2 multi-repo runs, so it was polling `st handoff show` while waiting for it.
* Tokens did not differ (578k to 647k per run, multi-repo): waiting in a shell loop costs time but not tokens.

### Scorecard for the phase-7 predictions

| # | Prediction | Result |
|---|---|---|
| 1 | dev-a chooses at least two release classes | **Right** (three, 6 / 7 / 2) |
| 2 | H0: at least 2 of 5 incomplete or slow (over 300 s) | **Right** (4/5 slow, none incomplete) |
| 3 | H1 and H2: at most 1 of 5 | **Right** (0/5 each) |
| 4 | The H2 note matches the registry in 5 of 5 | **Right** |
| 5 | Monorepo 5/5 complete, any failure reported with cause | **Right** (5/5 in each condition, no failures) |

### What phases 6 and 7 say together

* **When the release class is predictable, no channel is needed** (phase 6: all 15 multi-repo runs were a major release, all completed in about 100 s except one 611 s outlier). **When it is a judgement call, a channel saves several minutes per handoff** (phase 7), and a required note is as good as free messages. In neither phase did the lack of a channel produce a wrong or missing change; it produced waiting.
* **The registry is an implicit channel.** A team without a message system still has the registry, the PR list and the CD results. The failure to expect from a missing channel is a developer waiting on the wrong signal, not a developer getting the wrong answer.
* **The board is only as good as the habit of updating it.** Every no-channel developer who relied on task state lost time to a stale board.

### Limits specific to phases 6 and 7

* The agents poll with shell loops, so the "waiting" is partly a property of how these agents wait. A person would more likely message a colleague or look at the registry, which could shrink the H0 penalty, or leave a branch idle, which could grow it.
* Two developers, one dependency, a 90-second job. Real handoffs cross time zones and hours.
* All 30 phase-7 runs were complete; the study cannot say whether a wrong guess about the class would ever produce a wrong deployment, because the registry made the real release visible to every dependent developer.
* H2 posted one note per run; the quality of a note was not varied.
* Phase 6 and phase 7 conditions were not run concurrently with the single-developer arm.

---

# Phase 8: work breakdown into an epic with ordered child tickets (L3)

**Pre-registered 2026-10-31 before the tooling was built and before any phase-8 run.** Every earlier ticket was one ticket, with sub-tasks listed inside it. The plan's L3 lever is "single ticket versus an epic with ordered child tickets". The question: does splitting the same content into child tickets, each worked and closed separately, change whether the hidden app gets done?

## Design

The policy change (C3), the original 5-repository field, both layouts, one developer (Sonnet), 5 replicates, tag `s8`. The ticket is an **epic** whose description and epic-level acceptance criteria are the same as before ("every app that calls `validateApp` passes its owning team"), with **ordered child tickets**: the developer opens each with `st ticket <id>`, marks it done with `st ticket done <id>` when its change is live, and cannot close the epic with `st done` until every child is done.

| Arm | Child tickets | Single-ticket analogue (phase 1) |
|---|---|---|
| **E1** | contract, billing, shell (reports missing) | A2 (4 of 5 multi-repo misses) |
| **E2** | contract, billing, shell, reports | A3 (0 of 5) |
| **E3** | as E1, plus a **last child ticket "Verify the epic: confirm every app that calls `validateApp` has been updated, and fix or report any that has not"** | none (a breakdown that includes a verification step) |

15 rounds (30 runs).

## Predictions (recorded before data)

1. **E1**: at least 4 of 5 multi-repo runs miss the hidden app (child tickets narrow scope at least as much as a task list).
2. **E2**: 0 of 5.
3. **E3**: at most 2 of 5 miss (a verification child prompts a sweep; less than a full fix because the developer can mark it done after a shallow look).
4. **Monorepo**: 0 misses in every arm.
5. Epic arms cost at least 10% more tokens and at least 10% more time than their single-ticket analogues in the multi-repo layout (the extra ticket handling).

---

# Phase 9: noisy tickets

**Pre-registered 2026-10-31 before the tooling was built and before any phase-9 run.** The tickets so far were clean, template-generated text. Real tickets are often terse, rambling or stale. This phase degrades the **open-ended** ticket (the arm that was always safe, A1) in three ways and asks whether it stays safe.

## Design

Policy change (C3), original 5-repository field, both layouts, Sonnet, 5 replicates, tag `s9`, three arms, 15 rounds. Control: the clean open-ended arm A1 from phase 1 (multi-repo 0 of 5 misses; 5.0 repositories cloned; 161 s median; 379k tokens).

| Arm | The ticket |
|---|---|
| **N1 terse** | one short paragraph: "`validateApp` should require an owner. Apps pass their team (it's in package.json). Release per team rules." No acceptance criteria, no "every app" |
| **N2 rambling** | a pasted chat thread of about eight messages: the requirement (every app must declare an owner, `validateApp` should throw without one, apps pass their package.json `team`, it is breaking so major) buried among unrelated remarks about CI speed, README bucket names and a deadline. No list of apps, no acceptance criteria |
| **N3 stale name** | clean text, with the shared library named by an old name that no longer exists (`libs-config`, or `libs/config` in the monorepo); standard acceptance criteria; no list of apps |

## Predictions (recorded before data)

1. **N1**: at least 1 of 5 multi-repo runs misses the hidden app (the "every app" wording is gone).
2. **N2**: 0 of 5 misses, and at least 15% more tokens than clean A1.
3. **N3**: 0 of 5 misses; the developer resolves the old name from `st repos`; time within 20% of clean A1.
4. **Monorepo**: 0 misses in every arm.
5. Every noisy arm is complete (all three apps live) in at least 12 of 15 runs, both layouts together.

---

## Phase 8 results (30 runs, 15 rounds, run 07:54 to 08:41)

All 30 runs valid, none excluded. Controls are the single-ticket arms from phase 1 (A2 partial list, A3 complete list). Full table: `analysis-phase89.md` in the data folder. Because epics produced a failure the scorer did not distinguish, the analysis splits "an app left **unfixed**" from "an app updated with a **wrong owner value**".

| Arm | Layout | Complete, right values | App left unfixed | Wrong owner value | Opened the hidden repo | Child tickets opened / closed (mean) | Tokens k | Turnaround, median |
|---|---|---|---|---|---|---|---|---|
| **E1** epic, children without reports | multi | 3/5 | 1/5 | 1/5 | 5/5 | 2.6 / 3.0 | 424 | 150 s |
| | mono | 4/5 | 0/5 | 1/5 | 0/5 | 1.8 / 3.0 | 321 | 61 s |
| **E2** epic, children incl. reports | multi | 5/5 | 0/5 | 0/5 | 5/5 | 2.6 / 4.0 | 420 | 166 s |
| | mono | 5/5 | 0/5 | 0/5 | 0/5 | 2.0 / 4.0 | 377 | 65 s |
| **E3** epic, partial + final "verify" child | multi | 5/5 | 0/5 | 0/5 | 5/5 | 4.0 / 4.0 | 483 | 160 s |
| | mono | 3/5 | 0/5 | 2/5 | 0/5 | 2.4 / 4.0 | 339 | 60 s |

Controls (single ticket, multi-repo): A2 partial list 4/5 missed (344k tokens, 127 s); A3 complete list 0/5 (389k, 148 s).

### What it means

1. **Breaking the work into child tickets did not make the hidden-app miss worse.** With the same partial list, the epic arm missed the unlisted app in 1 of 5 multi-repo runs (the app was left entirely unfixed once; Fisher p = 0.52 against the single-ticket 4 of 5, so a lead, not a result). Every epic multi-repo run opened the reports repository (5 of 5, where the single-ticket partial list opened it in 2 of 5). A plausible reading is that moving a partial list into separate tickets makes it look more like a plan than a boundary, but I have no test of that.
2. **A final "verify the epic" child ticket fixed it** (E3: 0 of 5 unfixed, 5 of 5 complete in the multi-repo layout; against A2's 4 of 5, p = 0.048). It is the same remedy as the B1 instruction ("find every app that uses it") written as a ticket. It cost the most: 483k tokens against 344k for the single ticket (+40%) and 160 s against 127 s (+33 s, 95% interval [19, 55] s).
3. **A new failure: child tickets closed without being read.** 33 child tickets were closed over the 30 runs without ever being opened. All four runs with a **wrong owner value** closed the consumer child tickets unread; those children are where the instruction "use the team recorded in package.json" lives. The agents did the work from the epic's description and the first child, invented owner names (`platform-team`, `billing-team`, `reports-team`) and marked the rest done. In the single-ticket form the same sentence sits in the document the agent has already read. So **the breakdown moved a necessary detail into a document that was easy to skip.** The monorepo showed it most (3 of 15 runs; 0 apps left unfixed), because one PR does everything and nothing forces a look at the children.
4. **The epic's close gate did nothing here** (0 refusals): the agents closed every child, opened or not, before closing the epic.
5. **Cost.** Epic arms cost 8% to 40% more tokens and 12% to 26% more time than the single-ticket analogues in the multi-repo layout.

### Scorecard for the phase-8 predictions

| # | Prediction | Result |
|---|---|---|
| 1 | E1: at least 4 of 5 multi-repo runs miss the hidden app | **Wrong.** 1 of 5 left it unfixed (2 of 5 by the original any-miss measure) |
| 2 | E2: 0 of 5 | **Right** |
| 3 | E3: at most 2 of 5 miss | **Right** (0 of 5) |
| 4 | Monorepo: 0 misses in every arm | **Half right.** No app was left unfixed (0 of 15), but 3 of 15 had wrong owner values, which the scorer counts as misses |
| 5 | Epic arms cost at least 10% more tokens and time | **Right for E1 (+23%, +18%) and E3 (+40%, +26%); E2 +8% tokens, +12% time** |

### Limits specific to this phase

* The epic is a design choice: the instruction about where the owner value comes from lives only in the child tickets. A version whose epic description carried every detail would probably not show the wrong values; I did not run it. The finding is about breakdown that relocates detail, not about epics in general.
* The scorer counted wrong values as misses, as it was built to (the ticket says what the value must be). The unfixed/wrong-value split was added after seeing the first failed run; it is reported in every table here.
* Five runs per arm, one model.


## Phase 9b results (10 runs, 5 rounds, run 09:22 to 09:34)

| Arm | Layout | Complete | Tokens k (mean) | Turnaround, median |
|---|---|---|---|---|
| N2b rambling thread, property name explicit | multi | **5/5** | 364 | 122 s |
| | mono | **5/5** | 332 | 61 s |

**With the name stated, the same thread, unrelated chatter and all, passes in 10 of 10 runs** (all multi-repo releases were major). So the 10 failures in N2 came from the property name being implicit, not from the length or the noise of the thread. It was my wording that left the name implicit, and the agents resolved the ambiguity the same way in all 10 runs (to `team`, the only identifier in backticks). A caveat: N2b was written after seeing N2, by the same author, with one line changed; it shows the explicit name is sufficient, not that nothing else in the thread mattered. Predictions: (1) at least 4 of 5 multi-repo complete: right (5); (2) at least 4 of 5 monorepo complete: right (5); (3) tokens within 15% of N3: right (364k against 338k, +8%).

**What phase 9 and 9b say together.** Noise that removes information (a terse ticket) or misnames something that can be looked up (a stale library name) did little. Noise that leaves an **identifier implicit** cost every run, consistently, because the agents all picked the same plausible reading and built a coherent change around it. A ticket that is clear enough for a person to infer the intent can still be ambiguous about a name that a check, a contract or a downstream consumer depends on. The one post-merge break in the study (terse ticket) was the same shape in a different place: the instruction left open how to read a value, and one run chose a method the bundler could not handle.


# Item 3 of the "still not done" list: a human in the loop

Not run: it needs people, and I cannot supply them. What I did is make it ready to run and comparable to phase 5: the human review kit (12 of the same cases, three conditions rotated across participants, a response sheet, a packet generator and a scorer that prints the agents' result on the same 12 cases beside the humans'). My predictions for it are recorded in the kit's README before any human data exists. Status: ready, not run.

## Phase 9 results (30 runs, 15 rounds, run 08:41 to 09:21)

All 30 runs valid. Control: the clean open-ended arm A1 from phase 1 (run on a different day; see the drift caveat). Full tables: `analysis-phase89.md`.

| Arm | Layout | Complete | Failure | Repos cloned | Tokens k | Turnaround, median |
|---|---|---|---|---|---|---|
| A1 clean (control) | multi / mono | 5/5, 5/5 | none | 5.0 / 1.2 | 379 / 242 | 161 s / 59 s |
| **N1 terse** | multi | 4/5 | **1 post-merge break: all three apps stopped booting** | 5.0 | 332 | 122 s |
| | mono | 5/5 | none | 2.0 | 316 | 65 s |
| **N2 rambling thread** | multi | **0/5** | **all 5: the contract checks `app.team`, not `app.owner`** | 5.0 | 355 | 125 s |
| | mono | **0/5** | **all 5: the same** | 2.0 | 378 | 62 s |
| **N3 stale library name** | multi | 5/5 | none | 5.0 | 338 | 127 s |
| | mono | 5/5 | none | 2.0 | 283 | 59 s |

### What it means

1. **Two of the three kinds of noise did little.** A stale library name (N3) was resolved from `st repos` every time (10 of 10 complete). A terse ticket with no acceptance criteria and no "every app" (N1) still found all three apps in 10 of 10 runs, and cost slightly less than the clean ticket.
2. **The terse ticket produced the first post-merge break in the whole study.** In one multi-repo run the agent wrote `import pkg from '../package.json' with { type: 'json' }` to read the team at runtime, which the project's bundler cannot inline, and all three live apps stopped booting. CI was green because CI builds the bundle and never runs it. The clean tickets name the field (`team` in the app's `package.json`) and the agents turned that into a hard-coded literal; "(it's in package.json)" may have invited the runtime read, but one run cannot show that. One in 30 noisy runs, so this is an observation, not a rate.
3. **The rambling thread failed every run, for a specific reason.** In all 10 N2 runs the agent changed `validateApp` to require `app.team` and did not mention `owner` in the contract, then passed `team` values in the three apps. The work was consistent and the apps ran; it was built around a different property name from the one the clean tickets (and the scorer) use. The thread named `owner` only in prose ("nothing enforces that", "throw if there's no owner") and the package.json field `team` in backticks, the last identifier in the message. **Whether that is the agent's misreading or my ambiguous drafting, I cannot say from N2 alone;** phase 9b changes only that line to find out.
4. **Time and tokens.** All three noisy arms were 21% to 24% faster than the clean control in the multi-repo layout and used 6% to 12% fewer tokens. I do not read that as an effect of noise: the controls from the later phases of the previous afternoon are about as fast (A1 at 17 repositories 135 s, A3 126 s), so the phase-1 control, run earlier still, may carry drift. This cannot be separated from a real effect without a concurrent clean arm, which I did not run.

### Scorecard for the phase-9 predictions

| # | Prediction | Result |
|---|---|---|
| 1 | N1: at least 1 of 5 multi-repo misses the hidden app | **Right by count (1 of 5), wrong in kind:** it was a break, not a missed app |
| 2 | N2: 0 of 5 misses, and at least 15% more tokens than clean | **Wrong on both:** 5 of 5 failed (property name); tokens 6% lower |
| 3 | N3: 0 of 5 misses, time within 20% of clean A1 | **Misses right; time -21%** (drift, above) |
| 4 | Monorepo 0 misses in every arm | **Wrong:** N2 failed 5 of 5 in the monorepo too |
| 5 | Every noisy arm complete in at least 12 of 15 runs | **Wrong for N2** (0 of 10); N1 9 of 10, N3 10 of 10 |


---

# Phase 9b: the rambling thread with the property name made explicit

**Added 2026-10-31 after seeing the phase-9 N2 result, so it is not a pre-registered arm of the original design.** Every N2 run (10 of 10, both layouts) made `validateApp` check `app.team`, not `app.owner`, and failed the scorer on that. The thread named `owner` only in prose and the package.json field `team` in backticks. That is either a real effect of a conversational ticket or an ambiguity in the thread I wrote. This arm separates the two.

**N2b:** the same thread, with one line changed so the property is explicit: "`validateApp` should throw if there is no `owner`, and apps pass their team as the owner (the `team` field in their package.json)". Everything else, including the unrelated chatter, is unchanged. C3, both layouts, Sonnet, 5 replicates, tag `s9b`.

**Predictions (recorded before running):**

1. N2b multi-repo: at least 4 of 5 complete (the noise is harmless once the name is explicit).
2. N2b monorepo: at least 4 of 5 complete.
3. Token cost within 15% of N3 (the clean-text noisy arm).
