# Figure captions and sources

All three figures are built by `verification/scripts/figures.py` (Python standard library only) from the raw per-run results in `data/results/`. Every plotted number is read from those files when the script runs. Nothing is typed in. Re-run with:

```
cd verification/scripts && python3 -I figures.py ../../figures
```

Each SVG is 600 px wide and has a title and a text description for screen readers. The PNGs are the same figures at 1200 px (2x). Colours are from the Okabe-Ito palette, which stays distinguishable under the common forms of colour-blindness. Colour is never the only code: each series also has a different fill pattern, and every bar has its count written next to it.

## Figure (a): `fig-a-misses-by-ticket-and-layout.svg`

**Caption.** Runs left unfinished, by ticket and repository layout. For a rename (C2) and a policy change (C3), the number of runs out of 5 in which at least one app was not updated and live, for seven tickets, in a monorepo and in a multi-repo layout. The monorepo had none. The multi-repo had 4 of 5 with a partial list, 5 of 5 with a decoy list and 5 of 5 with per-repository checks on a partial list (policy change), and 2 of 5 for the per-repository-checks ticket on the rename.

**Report location.** Section 3.2, after the table.

**Source.** `results/s2-C{2,3}-A{1..7}-{mono,multi}-r{1..5}/summary.json`, field `acceptance_pass` (false = unfinished). Phase 1, main model, 5 runs per bar (140 runs). Matches the section 3.2 table and `results/analysis.md`.

**Note on scope.** C1 (additive change, one app affected) is left out: 0 misses in 20 runs, stated in the footer line.

**Text description.** Grouped horizontal bars, two panels. Monorepo bars are 0 in every row of both panels. In the rename panel the multi-repo bar is 2 for the checks-on-partial-list ticket and 0 elsewhere. In the policy-change panel it is 4 for the partial list, 5 for the decoy list, 5 for checks on a partial list, and 0 for the open-ended, complete-list and catalog tickets.

## Figure (b): `fig-b-mechanism-cloned-vs-finished.svg`

**Caption.** Cloned the missing app's repository versus finished the change. Multi-repo policy-change runs. For each ticket, the number of runs that cloned the missing app's repository (dotted bar) and the number that finished with every app updated (solid bar). Open-ended tickets and the three fixes cloned it and finished in every run. Partial-list tickets often cloned it and still did not finish. With 17 repositories, 4 of 5 partial-list runs cloned it and none finished. On the smaller model, partial-list runs never cloned it. The bottom bar splits all 33 incomplete changes in phases 1 to 4: 12 cloned the missing app's repository and left it unchanged, and 21 never cloned it.

**Report location.** Section 3.3, after the new table.

**Source.** `summary.json` per run, fields `repos_cloned` (from the harness's `clone` events), `acceptance_pass`, `topology = multi`, `change = C3`. Panels: phases 1 and 2 (tags `s2`, `s3`; 5 runs per bar), phase 3 (`s4`; 17-repository estate), phase 4 (`s5`; smaller model, 4 runs per bar). The missing app is `reports`, except arm A2s, where it is the core shell. The bottom bar uses all multi-repo runs in tags `s2`, `s2h`, `s3`, `s4`, `s5` with `acceptance_pass` false (33).

**Caveats.** "Cloned" means an `st clone` event. The harness kept no tool-call transcript, so a repository read in some other way would not show. The 12 and 21 are verified run by run in `claim-check.md`. The smaller-model phase-1 subset (`s2h`, one run per cell) is in the bottom bar only.

**Text description.** Three panels of paired bars and one stacked bar. In the five-repository panel, eight of twelve tickets show equal cloned and finished counts (seven at 5 of 5, and the core-shell variant at 3 of 5). The other four, all partial-list tickets, show cloned 2 of 5 (A2, A4, A7) or 4 of 5 (B3) and finished 1, 0, 0 and 1.

## Figure (c): `fig-c-timeline-of-phases.svg`

**Caption.** Timeline of the study: nine phases, 456 developer runs and 300 reviews. Each bar spans the first to the last recorded event of its phase, in US Eastern clock time, on 30 and 31 October 2026. The overnight gap is removed. The left column gives the number of runs (reviews for phase 5). Phase 9b was added after phase 9.

**Report location.** Section 2.7, after the phase table.

**Source.** Phases 1 to 4 and 6 to 9b: earliest `start_ms` in `meta.json` and latest `ts` in `events.jsonl` of each phase's runs (tags `s2`+`s2h`, `s3`, `s4`, `s5`, `s6`, `s7`, `s8`, `s9`, `s9b`). Run counts from the number of `summary.json` files. Phase 5: start and finish from `results/reviews-driver.log` (20:58:21 to 21:04:36); count from the 300 files in `review/out/`.

**Differences from the draft's section 2.7 table.** Phase 5 ends 21:04 here, 21:09 in the draft (no source found for 21:09). Phases 2, 3, 4 and 9 end one minute earlier here than in the draft; the other end times match. Run counts match.

**Text description.** One horizontal bar per phase on a clock axis. Phase 1 runs 07:51 to 12:23 on 30 October; phases 2, 3 and 4 follow until 18:10; phase 5 (reviews) takes about 6 minutes around 21:00; phases 6 and 7 (two developers) run 21:41 to 23:31; after the gap, phases 8, 9 and 9b run 07:54 to 09:34 on 31 October.
