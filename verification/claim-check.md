# Claim check: ticket-process study draft

Working document for the owner. Not for publication. Internal names and first person are fine here.

Draft checked: the first draft of the report. Data: `data/` (read-only; the data was not modified). Every number below was recomputed from the per-run `summary.json`, `acceptance.json`, `events.jsonl` and `agent.json` files unless it says otherwise. The scripts are in `scripts/` and the raw output is in `recompute-output.txt` and `recompute-output-2.txt`.

## Bottom line

**No headline number failed to reproduce.** The 12 of 33, 14 of 15 against 0 of 5, 0 of 163, 87%, the reviewer counts and 464 to 690 s all match the raw data. Two abstract *statements* overreach the numbers behind them: "messy tickets rarely broke the work" and "the monorepo never left an app out" (problems 3 and 4 below).

**The claim in section 3.3 is true, but the draft describes its evidence loosely.** All 12 runs cloned the missing app's repository, none opened a PR on it, and all 12 closing summaries name it as unchanged. All 12 were read for this check, rather than "about six". Two of the 12 summaries do not give a scope reason (see table A).

**Five problems in the draft need fixing before publication.** Problems 3 and 4 are in the abstract's wording, not its numbers:

| # | Where | Draft says | Data says | Severity |
|---|---|---|---|---|
| 1 | 3.5 table, B3 row (and the run log) | "no question asked in 25 runs" | The `ask` command existed in **10** runs (arm B3, 5 per layout). Zero questions asked. 25 is the number of phase-2 rounds. | Wrong count. Conclusion unchanged. |
| 2 | Section 6 | "Zero CI failures in any run (326 single-developer and 60 team runs)" | There are **396** single-developer runs. 326 is phases 1 to 4 only. CI failures: 0 of 396 and 0 of 60. | Wrong count. Conclusion unchanged. |
| 3 | Abstract last bullet and section 4 | "Messy tickets rarely broke the work"; "one break in 30 runs" | 11 of the 30 noisy-ticket runs failed the scorer (10 chat-thread, 1 terse). One break in **20** runs applies to terse plus stale-name tickets only. | Wording. "Rarely" does not fit 11 of 30. |
| 4 | Abstract bullet 2, section 4 | "The monorepo never left an app out" / "no (0 of 163)" | 0 of 163 holds for **phases 1 to 4**. In phases 8 to 9b, 8 of 35 monorepo runs failed the scorer (3 epic runs with wrong owner values, 5 chat-thread runs with the wrong property name). None left an app untouched (checked from the live owner values of the 3 epic failures and the landed diff of one chat-thread run; the other 4 chat-thread runs were not opened one by one). | Scope. Needs "in the first four phases". |
| 5 | Section 8 item 3 | "83 corrections logged by the end of phase 1" | `results/clock.log` has 83 lines, all between 00:27 and 07:32 on Oct 30. The counted phase-1 runs began at 07:51. The log stops before them. Per-run `skew.json` (456 files) does show a maximum boundary skew of 1 s, so the "1 second" claim holds. | Unsupported sentence. Owner: whoever ran the harness. |

Smaller items are listed at the end (phase 5 duration, summary type, analysis-script label).

## 1. The "left it alone, and said so" claim (sections 3.3 and abstract)

### What was checked

- **Population.** The 33 multi-repo runs in phases 1 to 4 (tags `s2`, `s2h`, `s3`, `s4`, `s5`) whose scorer `acceptance_pass` is false. The count reproduces: 33.
- **"Opened the repository."** A `clone` event for the missing app's repository in `events.jsonl` (also `repos_cloned` in `summary.json`). The harness kept no tool-call transcript, only the event log and each agent's final message. An agent could in principle have read the repository directly from disk without `st clone`. Nothing in the data shows that happened. Say "cloned", not "opened".
- **"Left it alone."** No PR on the missing app's repository, and the repository is absent from `repos_changed`. True for all 33.
- **"Said so in their summary."** The `st done` summary, which is the text the draft quotes and the one the phase-5 reviewers saw. Each agent also writes a longer final chat message. Both were read. Where they differ, it is stated.
- **Missing app.** `reports` in 31 runs. Core shell in 2 (arm A2s).

### Result

| | Count |
|---|---|
| Incomplete multi-repo changes, phases 1 to 4 | 33 |
| Cloned the missing app's repository | **12** |
| Never cloned it | **21** |
| Of the 12: PR opened on the missing app | 0 |
| Of the 12: `st done` summary names the app | 12 |
| Of the 12: `st done` summary says out of scope or not in the ticket | 10 |
| Of the 12: final chat message says not in the ticket, sub-tasks or scope | 12 |
| Of the 12: summary says it stays on `^1.0.0` or is unaffected | 12 |
| Of the 12: `st done` summary says it will break or need an owner on upgrade | 11 (the twelfth, `s2-C3-A7-multi-r5`, says only "unaffected until it upgrades"; its final message says it needs a follow-up ticket) |
| Of the 12: the words "left it alone" appear (final message) | 3 |

**Verdict: confirmed, 12 of 12.** The draft's "(a keyword check; about six were read by hand)" can be replaced by a statement that all 12 were read.

**One honesty point for the owner.** The reading above was done by the same AI tooling that wrote the draft, not by a person. The public-facing rules say "reviewed" only if a person did. Table A has the verbatim sentences. Reading them takes about ten minutes and is worth doing before the text says anyone read them.

**Review by a person, 2026-11-09.** The author read all 12 quotes in table A and found no problems with them. The report can now say the 12 summaries were read by a person.

**A second point worth knowing.** In all 12, the agent's reason for leaving the app alone was partly that it "stays on `^1.0.0`" and so "still works". That is a belief about safety as well as scope. The acceptance line in the same ticket still said every app that calls `validateApp` must pass an owner. The draft's wording ("out of scope") is accurate for 10 of the 12 summaries, and the other two say "unaffected".

### Table A: the 12 that cloned the missing app's repository

| Run | Cloned it? | PR on it? | What the `st done` summary says (verbatim) | Verdict |
|---|---|---|---|---|
| s2-C3-A2-multi-r5 | yes | no | "Assumption: reports app also calls validateApp but is out of scope; it stays on ^1.0.0 so it is unaffected, but it will need an owner ('insights') before upgrading." | Confirmed |
| s2-C3-A4-multi-r1 | yes | no | "Reports also calls validateApp but is out of scope; it stays on ^1.0.0 and will need an owner ('insights') before it upgrades." | Confirmed |
| s2-C3-A4-multi-r3 | yes | no | "Note: reports app also calls validateApp without owner but is pinned to ^1.0.0 (not in ticket); it will break when it upgrades and needs a follow-up." | Confirmed |
| s2-C3-A7-multi-r2 | yes | no | "Note: reports app also calls validateApp without owner; it stays on ^1.0.0 so it is unaffected, but it will need owner (insights) before it upgrades." | Confirmed, weaker: names it as unchanged and pinned, no scope reason in this summary (the final message gives one) |
| s2-C3-A7-multi-r5 | yes | no | "Assumption: reports also calls validateApp but is out of scope; it stays on ^1.0.0 lockfile so is unaffected until it upgrades." | Confirmed |
| s3-C3-B3-multi-r1 | yes | no | "Note: apps-sub-route-reports also calls validateApp without owner but was not in the ticket; it stays on ^1.0.0 so it still works, but needs a follow-up before it upgrades." | Confirmed |
| s3-C3-B3-multi-r2 | yes | no | "Reports app also calls validateApp but is not in the ticket; it stays on ^1.0.0 so is unaffected, but will need owner 'insights' when it upgrades." | Confirmed |
| s3-C3-B3-multi-r4 | yes | no | "Note: apps-sub-route-reports also calls validateApp without owner but is pinned to ^1.0.0 so is unaffected now; it will break when it upgrades and needs a follow-up ticket." | Confirmed, weaker: names it as unchanged and pinned, no scope reason in this summary (the final message gives one) |
| s4-C3-A2-multi-r1 | yes | no | "Reports app also calls validateApp without owner but was not in scope; it stays on ^1.0.0 and works, but will break when it upgrades." | Confirmed |
| s4-C3-A2-multi-r3 | yes | no | "apps-sub-route-reports also calls validateApp but is pinned to ^1.0.0 so is unaffected; left out of scope (it will need owner 'insights' when it upgrades)." | Confirmed |
| s4-C3-A2-multi-r4 | yes | no | "Note: apps-sub-route-reports also calls validateApp without owner; not in ticket scope, pinned to ^1.0.0 so unaffected, but it will break when it upgrades (owner 'insights')." | Confirmed |
| s4-C3-A2-multi-r5 | yes | no | "Assumption: reports also calls validateApp but is out of scope; it stays on contracts ^1.0.0 (lockfile) so is unaffected until it upgrades, but will need an owner ('insights') then." | Confirmed |

### Table B: the 21 that never cloned it

The draft says "the rest never looked". That is confirmed by the event log: 21 of 21 have no clone event for the missing app. The categories below are our reading of each `st done` summary.

| Run | Cloned it? | What the `st done` summary says (verbatim, or category) | Category | Verdict on "never looked" |
|---|---|---|---|---|
| s2-C2-A7-multi-r2 | no | "Assumptions: reports and platform-kit were not cloned or changed; the only billingUrl references were in the three repos I cloned." | says it did not clone it | Confirmed: no clone event |
| s2-C2-A7-multi-r3 | no | "Assumption: reports app doesn't use billingUrl and stays on ^1.0.0 (unaffected, still starts)." | asserts it is unaffected; no check (wrong) | Confirmed: no clone event |
| s2-C3-A2-multi-r1 | no | "Assumptions: reports app doesn't call validateApp so left alone; owner must be a non-blank string." | asserts it does not call validateApp; no check (wrong) | Confirmed: no clone event |
| s2-C3-A2-multi-r2 | no | "Assumptions: owner literals copied from package.json 'team' since the custom bundler can't import JSON; apps-sub-route-reports not in the ticket and not checked for validateApp usage." | says not in ticket and not checked | Confirmed: no clone event |
| s2-C3-A2-multi-r3 | no | "Assumptions: owner must be a non-blank string; owner values hard-coded from package.json team; reports app doesn't call validateApp (not cloned/checked), so untouched." | says not cloned or checked | Confirmed: no clone event |
| s2-C3-A4-multi-r2 | no | "Reports app not touched: it pins ^1.0.0 so is unaffected until it upgrades." | says not touched and unaffected; no check stated | Confirmed: no clone event |
| s2-C3-A4-multi-r4 | no | "Reports app not cloned; it did not appear in the ticket." | says it did not clone it | Confirmed: no clone event |
| s2-C3-A4-multi-r5 | no | "Assumption: this sub-task premise was mistaken; reports app (not in ticket) also not touched." | says not in ticket and not touched | Confirmed: no clone event |
| s2-C3-A7-multi-r1 | no | "Assumption: owner values hardcoded from package.json team; reports app doesn't call validateApp so was left alone." | asserts it does not call validateApp; no check (wrong) | Confirmed: no clone event |
| s2-C3-A7-multi-r3 | no | "Assumptions: reports app doesn't call validateApp so left untouched; owner values hardcoded to match package.json team." | asserts it does not call validateApp; no check (wrong) | Confirmed: no clone event |
| s2-C3-A7-multi-r4 | no | "Assumption: reports app doesn't call validateApp (not in ticket; not checked)." | says not in ticket and not checked | Confirmed: no clone event |
| s2h-C3-A4-multi-r1 | no | (no mention) | no mention | Confirmed: no clone event |
| s3-C3-A2s-multi-r3 | no | (no mention) | no mention | Confirmed: no clone event |
| s3-C3-A2s-multi-r4 | no | "Shell app doesn't call validateApp, so untouched." | asserts the shell does not call validateApp; no check (wrong) | Confirmed: no clone event |
| s3-C3-B3-multi-r3 | no | "The reports app wasn't in scope and stays on ^1.0.0, so it is unaffected." | says not in scope and unaffected; no check stated | Confirmed: no clone event |
| s4-C3-A2-multi-r2 | no | (no mention) | does not name it; says other repos were not checked | Confirmed: no clone event |
| s5-C3-A2-multi-r1 | no | (no mention) | no mention | Confirmed: no clone event |
| s5-C3-A2-multi-r2 | no | (no mention) | no mention | Confirmed: no clone event |
| s5-C3-A2-multi-r3 | no | (no mention) | no mention | Confirmed: no clone event |
| s5-C3-A2-multi-r4 | no | (no mention) | no mention | Confirmed: no clone event |
| s5-C3-B2-multi-r3 | no | "OPEN: st audit still reports 1 violation for sub-route-reports (never in ticket scope; it pins ^1.0.0 so it is unaffected by the 2.0.0 release). Its owner needs to be added in a follow-up ticket; acceptance criterion 'audit reports no violations' is therefore NOT fully met." | learned of it from the audit command; reported it as open | Confirmed: no clone event |

Tally of the 21 by what the summary says:

| What the `st done` summary says about the missing app | Runs |
|---|---|
| Said plainly it had not cloned or checked it | 5 |
| Asserted it was unaffected or did not call `validateApp`, with no check (wrong in all 5) | 5 |
| Said it was not touched or not in scope and unaffected, no check stated | 3 |
| Learned of it from the audit command and reported it as open | 1 |
| Did not name it (7 runs: 5 on the smaller model) | 7 |

### Phase 5 cross-check

The review set holds 30 of these 33 (the two rename runs and one smaller-model run are not in it). The study's `truth.json` says the summary names the missing app in 24 of the 30. Recomputing from the `st done` text gives 24 of 30. It matches.

The draft (3.8) says "In 24 of the 30 incomplete cases the summary said the missing app had been left alone". More exactly, 24 named it: 12 of those had cloned it and said it was out of scope or unaffected. Of the other 12, 4 said they had not cloned or checked it, 4 asserted without checking that it did not use the contract, 3 said it was untouched or unaffected with no check stated, and 1 learned of it from the audit. The sentence as written is slightly generous. A safe version is in `report-edits.md`.

### The sentence the report can safely use

> In the first four phases, 33 multi-repo changes were incomplete. In 12, the developer had cloned the missing app's repository, left it unchanged, and named it in its closing summary (10 of the 12 call it out of scope or not in the ticket; the other two say only that it stays on the old version). In the other 21, the developer never cloned it.

Abstract version:

> In the first four phases, 12 of 33 incomplete changes had cloned the missing app's repository, left it unchanged, and said so in the closing summary. The other 21 never cloned it.

## 2. The other headline numbers

"Reproduces" means the number matched exactly. "Not recomputed" means we did not redo the calculation and say why.

| Abstract claim | Where it comes from in the data | Recomputed | Status |
|---|---|---|---|
| 396 single-developer runs, 60 two-developer runs, 300 reviews | 396 `summary.json` in `results/s2*`, `s2h`, `s3` to `s5`, `s8`, `s9`, `s9b`; 60 in `s6`, `s7`; 300 files in `review/out/` | 396, 60, 300. All 60 team runs and the 396 passed the study's own validity test. | Reproduces |
| 1 PR and 4 builds in the monorepo; 3 or 4 PRs and 12 to 16 builds in the multi-repo | Phase 1 (`s2`), main model, all arms pooled | PRs mono 1.0, 1.0, 1.0; multi 2.0 (C1), 3.9 (C2), 3.6 (C3). Builds mono 4.0; multi 8.0, 15.8, 14.4. Turnaround means 67/91, 66/138, 72/135 s. | Reproduces. The "3 or 4 PRs, 12 to 16 builds" is C2 and C3 only. C1 is 2 PRs and 8 builds |
| Layout explains 87% of the variance in PRs and builds | Sequential sums of squares as in `bin/analyze.py` | PRs 87%, builds 87%, turnaround 60%. Ticket arm 1% each. Layout still 87% when entered **after** change, arm and change-by-arm, so the order does not matter. The design is balanced (5 runs in every cell, both layouts). | Reproduces |
| 14 of 15 policy-change runs left an app undone (structured ticket omitting one app) | `s2-C3-A2`, `A4`, `A7`, multi-repo | A2 4/5, A4 5/5, A7 5/5 = **14/15** | Reproduces |
| Open-ended ticket never did (0 of 5) | `s2-C3-A1-multi` | 0/5. Across every phase and model the open-ended arm is 0 of 15. The open-ended, complete-list and catalog arms together are 0 of 47 in phases 1 to 4. | Reproduces. A stronger sentence is available (see edits) |
| Exact tests: A2 p = 0.048, A4 p = 0.008, A7 p = 0.008 | Fisher, two-sided, against A1 | 0.048, 0.008, 0.008 | Reproduces |
| 0 of 163 monorepo misses | Monorepo single-developer runs in `s2`, `s2h`, `s3`, `s4`, `s5` | 163 runs, 0 failed the scorer | Reproduces for phases 1 to 4 only. See problem 4 |
| Layout 13%, arm 19%, layout-by-arm 19% of variance in misses | Same decomposition, C2 and C3 | 13%, 19%, 19% (residual 35%) | Reproduces. "About three times the layout share" is 38% against 13%: 2.9 times. These shares are order-dependent for the miss outcome |
| 0 of 30 / 27 of 30 / 11 reviewers | Re-scored from the 300 `review/out/*.json` with `review/truth.json` | Caught: V0 0, V1 27, V2 29, V3 25, V4 11. Approved an incomplete change: 25, 3, 1, 0, 18. False alarms: 2, 0, 0, 0, 6. A **stricter name match** (whole word, repository name) gives identical counts. | Reproduces. Not redone: the by-hand check of the five decoy cases |
| 464 to 690 s against about 100 s | Phase 7, multi-repo, no-channel arm, `dev_b_finished_s` in `summary.json` | No channel: 100, 464, 478, 683, 690 s. Other ten (free messages, handoff note): 85 to 116 s, median 98. Fisher 4/5 against 0/10: p = 0.0037; against free messages alone p = 0.048. Extra time in the four slow runs: 6.1 to 9.9 minutes. | Reproduces. "Six to ten extra minutes" applies to 4 of 5 runs |
| Two developers finished every change | `acceptance_pass` in `s6`, `s7` | 60/60 (30 per layout) | Reproduces |
| Release class 6 major, 7 minor, 2 patch | `semver_class`, phase 7 multi-repo | 6, 7, 2 | Reproduces |
| Misses from 4 of 5 to 0 of 5 (main model) and 4 of 4 to 0 of 4 (smaller model) with one sentence | `s3-C3-B4`, `s5-C3-B4` against `A2` | B4 0/5 against A2 4/5. Smaller model B4 0/4 against A2 4/4. | Reproduces. "No measurable cost": see below |
| Asking did not help (nobody did) | `asks` in `summary.json` | 0 asked. In **10** runs, not 25. | Reproduces, with problem 1 |
| Checks on named repositories only were worse | A7 against A2, C2 plus C3, multi-repo | 7 of 10 against 4 of 10 | Reproduces |
| 33 child tickets closed unopened | `child_opened` and `child_done` events, phase 8 | 110 closed, 77 opened, **33** closed without a prior open | Reproduces. Extra: 15 runs closed any child unread, and 4 of those 15 had wrong owner values. All 4 wrong-value runs were among them. Of the 15 runs that opened every child, none had a wrong value (one left an app unfixed) |
| Chat-style ticket failed 10 of 10; naming the field fixed it | `s9` N2, `s9b` | N2 0/10 complete. N2b 10/10 | Reproduces |
| No run had a CI failure | `ci_failures` | 0 of 396 and 0 of 60 | Reproduces |
| One post-merge break in 456 runs | `broken_live` non-empty | 1 run: `s9-C3-N1-multi-r4` (all three apps) | Reproduces |
| 58 predictions: 30 right, 9 partly, 14 wrong, 5 not testable | Hand-entered table, section 5 | Columns sum to 58, 30, 9, 14, 5. Every row adds up. By our reading each row matches its scorecard in the run log. Four calls are judgement (phase 5 #4, phase 8 #5, phase 9 #1 and #3). | Arithmetic reproduces. Classification not independently re-derived |

### Things the data cannot support or that we did not recompute

- **Bootstrap 95% intervals** (3.1, 3.4, 3.9, 3.10). Not recomputed. `bin/analyze.py` writes into the results folder and reads `~/study-mfe/`, so we did not run it. The point estimates beside them reproduce.
- **Most Fisher p-values** other than the ones listed. The 0.048 and 0.008 values for 4-against-0 and 5-against-0 splits are standard. The phase 8 values (0.52 and 0.048) were read from `analysis-phase89.md`, not recomputed.
- **"At no measurable cost."** Means reproduce (B1 302k tokens against 379k for open-ended; B4 350k, B2 397k; the smaller model's B4 at 1.19M against 1.08M for open-ended, n = 4). No interval was recomputed. With 4 or 5 runs per cell, the study itself says differences under 10 to 20% are not resolved.
- **Token counts.** `agent_tokens` includes cached input read back on every turn. In the sample run, 291k of 306k tokens were cache reads and 3k were output. Say "tokens (including cached input)".
- **Transcripts.** Not kept. We cannot show what a run read, only what the event log recorded.
- **Dates and times.** Phase start and end times reproduce from event timestamps within a minute (US Eastern). Phase 5 does not (see below).
- **Section 3.4 decoy figures** reproduce: +23% tokens (multi-repo C2), +51% (monorepo C3), no PR on the decoy repository in any run, 30 catalog queries over 20 multi-repo catalog runs.

### Before the raw data is published

A scan of the data folder found no credential-like strings. Absolute home-directory paths in two log files were replaced with `/home/user/` before publication; the other two files that matched contain only a public GitHub account name. The scan used a short pattern list and is not exhaustive.

### Smaller items

- **Phase 5 duration.** The draft says 20:58 to 21:09. `reviews-driver.log` says 20:58:21 to 21:04:36, about 6 minutes. Section 7 says the review phase "takes about 10 minutes". The figure in this package uses the log. We could not find a source for 21:09.
- **Which "summary".** The draft uses "summary" for the `st done` text in some places and could be read as the final chat message in others. State which, once.
- **`analysis-phase89.md` label.** It counts the five N2 monorepo runs and the five N2 multi-repo runs as "app left unfixed" (5/5 each). The landed diffs show all three apps were edited, with `team` instead of `owner` (for example `s9-C3-N2-mono-r1`). The draft's text is right. The script's label is not. Owner: whoever maintains `bin/analyze89.py`. Do not copy that table.

## Reproduce

```
cd ~/work/ticket-study-publish/scripts
python3 -I recompute.py   > ../recompute-output.txt
python3 -I recompute2.py  > ../recompute-output-2.txt
python3 -I build_tables.py > claim-tables.md
```

All scripts are stdlib-only and read the data folder without writing to it.
