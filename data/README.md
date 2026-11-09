# Study scripts and raw results (s2)

> **Scrub note (2026-11-07):** before publication, the absolute home-directory path of the machine that ran the study was replaced with `/home/user/` in `results/matrix.log` and `results/matrix-overnight-auth-failed.log`. Nothing else was changed. A scan found no credentials or private keys; the e-mail addresses in the data are fake `study.local` addresses. The repository paths still contain the owner's public GitHub handle.

Copy of `~/study-mfe/s2/` taken 2026-10-30 after all nine phases (8, 9 and 9b added below). Write-up and results: [the run log](run-log.md). Plan: [the pre-registration](pre-registration.md). Field and method inherit from [the first study](https://dlockamy.com/posts/2026/11/05/testing-the-monorepo-argument/) (its data).

**Left out on purpose:** `snap/` (the Jenkins/registry/S3 snapshot, ~145 MB; rebuild with `bin/build-field.sh`, about 3 minutes, needs `~/study-mfe/registry` and the `study-jenkins:local` image from the first study), `runs/` (everything useful is duplicated in `results/`), the agents' working clones (nested git repositories; landed diffs are in `results/*/landed-*.diff`), and `results/invalid-auth/` (156 empty failures from the overnight login expiry, described in the write-up).

**Where things are**
- `queue.json`: the 88-round queue. `bin/make-queue.py` makes it; `bin/run-matrix.sh` runs it; `bin/run-round.sh` runs one round (restore, two concurrent developers, score).
- `bin/gen.py`: ticket generator (arms A1-A7 by change type C1-C3). `bin/st2.sh`: the stand-in for GitHub and Jira (`st deps` catalog, `st ask` responder). `bin/accept2.cjs`: objective scorer that runs the live bundles. `bin/report2.py`, `bin/finish2.sh`, `bin/analyze.py`.
- `results/<run>/`: `summary.json`, `acceptance.json`, `events.jsonl`, `prs.json`, `ticket.md`, `agent.json` (tokens, cost, turns), `landed-*.diff`. `results/runs.csv`: one row per valid run. `results/analysis.md`: the full analysis output. `results/clock.log`: every Docker-VM clock correction.
- `results/archive*`, `results/matrix-overnight-auth-failed.log`: the pilot, the voided round and the overnight failure.

## Phases 2 to 4 (added after the first copy)

* Queues: `queue.json` (phase 1, 88 rounds incl. the smaller-model subset), `queue2.json` (phase 2, arms B1-B4 and A2s, tag `s3`), `queue3.json` (phase 3, 17-repository estate, tag `s4`), `queue4.json` (phase 4, smaller model, tag `s5`).
* Phase 2 additions: `gen.py` arms B1-B4 and A2s, `audit.py` and the `st audit` command in `st2.sh`. Phase 3 additions: `add-noise.sh` (the 12-repository estate), `st3.sh`, `new-run3.sh`, `run-round3.sh`, `run-matrix3.sh`, `field-restore3.sh`, `field-snapshot3.sh`, `finish3.sh` (copies of the phase-1 scripts pointing at `snap3`, so the phase-1/2 scripts were never edited while a run was live). Run a queue with `bash bin/run-matrix.sh <queue>.json` (`run-matrix3.sh` for phase 3), after starting `bin/clocksync.sh` in the background.
* Analysis: `bin/analyze.py s2` (phase 1), `analyze2.py`, `analyze3.py`, `analyze4.py`. Outputs: `results/analysis.md`, `analysis-phase2.md`, `analysis-phase3.md`, `analysis-phase4.md`, `results/runs.csv` (phase 1 only).
* `snap3/` is also left out (same reason as `snap/`); rebuild with `bin/add-noise.sh` on a restored field, then `bin/field-snapshot3.sh`.
* Run-directory name key: `s2` phase 1 (Sonnet), `s2h` phase-1 smaller model, `s3` phase 2, `s4` phase 3, `s5` phase 4. Format `<tag>-<change>-<arm>-<layout>-r<replicate>`.

## Phases 5 to 7 (added after the second copy)

* **Phase 5 (review):** `bin/build-review-cases.py` builds the 60 cases (ticket, combined diff, developer summary) from saved runs; ground truth goes to `review/truth.json`, outside the case folders; `bin/review-job.sh` and `bin/run-reviews.sh` run the 300 reviews (6 in parallel; no field needed); `bin/analyze5.py` scores them. Data: `review/cases`, `review/out` (the reviewers' raw JSON), `review/truth.json`, `results/analysis-phase5.md`.
* **Phases 6 and 7 (two developers):** `bin/st-team2.sh` (the team `st`, with the optional message channel and handoff note), `bin/new-team-run2.sh`, `bin/brief-team2.sh`, `bin/run-team-round.sh`, `bin/run-team-matrix.sh` (set `TEAM_CHANGE=C4` for phase 7), `bin/finish-team2.sh`, `bin/report-team2.py`, `bin/analyze67.py <tag> <output>`. Queues: `queue5.json` (phase 6, tag `s6`), `queue6.json` (phase 7, tag `s7`). Change C4 is in `bin/gen.py` and `bin/accept2.cjs`. Results: `results/s6-T-*`, `results/s7-T-*` (per run: both developers' agent JSON, events, PRs, messages and handoff notes, landed diffs), `analysis-phase6.md`, `analysis-phase7.md`.
* Run-name key: `s6-T-<H0|H1|H2>-<layout>-r<n>`, `s7-T-...`.

## Phases 8, 9 and 9b (added after the third copy)

* **Phase 8 (epics):** arms E1 to E3 in `bin/gen.py` (the epic ticket and its `children/` files); `bin/st4.sh` (the developer tool with `st ticket <id>`, `st ticket done <id>` and the close gate), `bin/new-run4.sh`, `bin/run-round4.sh`, `bin/run-matrix4.sh`; queue `queue7.json` (tag `s8`).
* **Phase 9 (noisy tickets):** arms N1 to N3 and N2b in `bin/gen.py`; queues `queue8.json` (tag `s9`) and `queue9.json` (tag `s9b`); `bin/run-phases-89.sh` ran phases 8 and 9 in sequence.
* Analysis: `bin/analyze89.py` (splits "app left unfixed" from "wrong owner value"; compares with the phase-1 controls) -> `results/analysis-phase89.md`.
* The human review kit is separate: README.
