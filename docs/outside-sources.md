# Ticket structure and process: outside views, and what the follow-up can test

Why this exists: the pre-registration [the pre-registration](pre-registration.md) says "outside views first" before locking. This is the same exercise as monorepo vs multirepo evidence, for levers L1-L6 and predictions 1-8. Nothing in the prereg was edited.

**How I read things.** Every source was reached through web search summaries and `WebFetch`, which returns a short model-written digest of a page, not the page. Most reads below are therefore **abstract or digest only**. I opened no full paper text. Where a number comes only from a search-engine summary, I say so. Several fetches failed (OpenAI's SWE-bench Verified post returned 403; TU Delft and Saarland repositories refused connections), so those are known only from search summaries.

## Bottom line

* **Almost nothing here is causal, and almost nothing studies our setting.** The human-process literature is observational (mining, surveys, single-company case studies). The agent literature is benchmark work, mostly on SWE-bench variants, with *synthetic* underspecification. No source I found tests ticket structure, a dependent catalog or a handoff template on agents making cross-repository changes.
* **Direction of evidence by lever.** Structured input and templates are associated with faster resolution (L1, L5), but with large confounds. Clarification helps agents when the ticket really is underspecified (L4). Misleading hints are followed by agents (L2 decoy). Extra instruction text can *hurt* agents (L1 heavy structure). Stale documentation is common, but I found no study that measures whether people or agents *trust* it.
* **Three things the survey adds that the prereg lacks:** a "ticket contains a wrong hint" level, a measurement of whether acceptance checks are strong enough to fail anything, and the cost of over-specification (tokens, steps). See the last section.
* **Effect sizes in the literature are small or contested** (breaking changes affecting about 8% of clients; socio-technical congruence null in a 25-project study). That supports a hard threshold like the prereg's 20 percent rule and warns against expecting large process effects.

## 1. Ticket structure, readiness gates, small batches, WIP (L1, L3)

| Source | What I read | Strength | What it supports |
|---|---|---|---|
| DORA, [Working in small batches](https://dora.dev/capabilities/working-in-small-batches/) | Page via digest | Guidance plus asserted survey research; the page gives **no statistics, sample sizes or methods**. Underlying reports cited: State of DevOps 2016, 2017, 2023 and the 2025 AI model | Small, independent, estimable batches (the page recommends INVEST) are claimed to predict delivery performance and to amplify AI gains. Supports L3 (breakdown) only as an assertion. I could not check the primary reports |
| Sjøberg, ESEM 2018, WIP in Kanban teams ([SINTEF](https://www.sintef.no/en/publications/publication/1637884/)) | Abstract via digest | Observational case study, one company, 5 teams, over 8,000 work items, 4 years | Lower WIP went with shorter lead time, but WIP also correlated with productivity (against the usual claim). No optimal limit found. Author says quality was not measurable and replication is needed |
| Sülün, Saçakcı, Tüzün, TOSEM 2024, issue templates ([Bilkent](https://repository.bilkent.edu.tr/items/a0c0b7c6-621e-4ca8-b17f-2843dfa072bf), [Crossref record](https://api.crossref.org/works/10.1145/3643673)) | Abstract via digest | Observational mining: 350 templates, 100 large OSS projects, over 1.9M issues, plus a maintainer survey | Projects with templates: resolution time reported as 381 days vs 103 days (the digest does not say mean or median), comments 4.95 vs 4.32; YAML (more structured) templates further cut reopenings. 99 of 100 projects use templates, so the comparison group is tiny and self-selected. Strongly confounded. Supports L1 and L5 directionally |
| Bettenburg et al., FSE 2008, "What makes a good bug report" ([review](https://neverworkintheory.org/2011/08/30/what-makes-a-good-bug-report.html)) | Third-party review via digest, not the paper | Survey, 466 responses from Apache, Eclipse, Mozilla developers and users; 289 rated reports | Developers most want repro steps, stack traces and test cases, which reporters find hardest to give. A scorer predicted quality for only 31-48% of reports. Supports an acceptance-check rubric score, and warns that real tickets lack the fields templates ask for |
| Méndez Fernández et al., NaPiRE ([arXiv 1611.10288](https://arxiv.org/abs/1611.10288)) | Abstract via digest; effects from a search summary of an aggregator page | Survey, 228 companies, 10 countries | Search summary says incomplete and hidden requirements rank first and lead to time overruns and post-implementation rework. I could not confirm the numbers |
| BDD reviews ([Binamungu and Maro mapping study, arXiv 2305.05567](https://arxiv.org/pdf/2305.05567v1) and others) | Search summaries only | Secondary studies; mapping study covers 166 papers | Reported benefit is mainly communication; defect-reduction evidence is perception-based and thin. Little support for "acceptance checks reduce rework" (prediction 6) beyond opinion |

**Against heavy structure.** I found no human-team study showing a definition-of-ready gate *harms* delivery. The counter-evidence is indirect: Sjøberg's mixed WIP result, and the agent finding in section 5 that added instruction text raises cost and does not raise success. Honest summary: the case *for* structure is common practitioner belief plus confounded observational data, and the case *against* is mostly absence of proof.

## 2. Dependency catalogs, ownership maps, code search; stale catalogs (L2, L6)

* **No study I found measures "catalog reduces missed dependents."** Searches for Backstage and catalog adoption returned only vendor documentation and blogs. Spotify's guidance (via search summary) is that metadata stays current when it lives next to the code. Roadie sells completeness scorecards. Treat all as **vendor or anecdote**.
* **Code search as the alternative to a catalog.** Sadowski, Stolee, Elbaum, [How developers search for code](https://research.google/pubs/how-developers-search-for-code-a-case-study/), ESEC/FSE 2015 (abstract via digest; survey plus logs at Google; a search summary gives 396 survey responses): about 5 sessions and 12 queries per workday; goals include "where code lives". One company, with Google-grade tooling. Consistent with the first study's finding that a monorepo grep found the hidden consumer (monorepo vs multirepo evidence, claim 3).
* **Hidden dependencies cause outages (weak).** A Huawei Cloud paper ([AID, arXiv 2109.04893](https://arxiv.org/pdf/2109.04893)) reports via search summary that improper service dependency was the most frequent failure cause in their incidents; a CACM piece says hand-drawn diagrams fail past about 100 microservices. Incident data from one provider and an opinion article.
* **Stale documentation is common.** Tan, Wagner, Treude, [Detecting Outdated Code Element References](https://arxiv.org/abs/2212.01479) (abstract via digest): over 3,000 GitHub projects, most had at least one outdated reference at some point. It measures staleness, **not whether readers were misled**. The "misleads users and developers" framing is the authors' premise.
* **Trust in stale docs:** my searches found no study measuring it. The prereg's prediction 2 (agents trust a stale catalog) rests on the agent-side evidence in section 5, not on human studies.
* **Coordination research is mixed.** Cataldo and Herbsleb (TSE 2013; search summary only) report that gaps between needed and actual coordination increased failures in two large projects. A 25-project replication attempt, Mauerer et al., [arXiv 2105.08198](https://arxiv.org/abs/2105.08198) (abstract via digest), found **no statistical relationship** of congruence with bugs or churn. So "know who depends on you and tell them" has contested empirical backing.

## 3. Release coordination for breaking changes (L2, L5; not a lever yet)

| Source | What I read | Strength | Finding |
|---|---|---|---|
| Ochoa et al., [Breaking Bad?](https://arxiv.org/abs/2110.07889) (EMSE 2021, replicates Raemaekers) | Abstract via digest | Observational mining: 119,879 library upgrades, 293,817 clients, Maven Central | 83.4% of upgrades comply with semver; only 7.9% of clients affected by breaking changes; most breaks touch code no client uses. Contrasts with the original Raemaekers finding (about a third of releases break, same for minor and major; known from a search summary only, original not opened) |
| Brito et al., [Why and how Java developers break APIs](https://arxiv.org/abs/1801.05198) | Abstract via digest; deprecation details from a search summary | Field study: 400 libraries watched about 4 months, 59 breaking changes confirmed by developers of 19 projects | Motives were features, simplification, maintainability. Search summary says most did not deprecate first because of maintenance cost. Small sample |
| He et al., [Dependabot exploratory study](https://arxiv.org/abs/2206.07230) (IEEE TSE) | Abstract via digest; numbers from a search summary | Mining plus survey; summary cites 1,823 projects and 502,752 updates | Technical lag dropped after adoption (summary: 48.99 to 25.38 days at 90 days); developers receptive; compatibility scores too scarce; 11.3% of projects dropped the bot |
| Rombaut, Cogo, Hassan, [Dependabot compatibility score](https://arxiv.org/abs/2403.09012) | Abstract via digest | Mining: 579,206 PRs | **No score for 83% of updates** (no crowd data). Recommends showing confidence and weighting test quality |
| Kula et al., [Do developers update?](https://arxiv.org/abs/1709.04621) (EMSE 2017) | Abstract via digest | 4,600+ projects, 2,700+ libraries, plus survey | 81.5% of systems keep outdated dependencies; 69% of surveyed developers did not know of vulnerable dependencies; updating seen as low priority. Note: 2017 data, library migration, not bots |
| Decan, Mens, Constantinou, [technical lag in npm](https://arxiv.org/abs/1806.01545) | Abstract via digest | 1.4M releases, 120K packages | Lag grows over time; semver constraints can reduce it |
| Hejderup and Gousios, [Can we trust tests to automate dependency updates?](https://arxiv.org/abs/2109.11921) (JSS 2022) | Abstract via digest | 521 Java projects (coverage), 262 projects with over 1.1M injected faults | Tests reach 58% of direct dependency calls; caught 47% of injected direct and 35% of indirect faults. A static impact tool found about twice as many. Green CI after an update is weak evidence |
| Pact and consumer-driven contracts: Ayas et al., SEAA 2022 ([Chalmers](https://research.chalmers.se/en/publication/534630)); Schwarz, Quast, Riehle, STVR 2025 ([PDF](https://dirkriehle.com/wp-content/uploads/2025/06/stvr-e70006.pdf)) | Search summaries only | 4 CDC repos qualitatively; one action-research study | CDC testing can ensure syntactic interoperability (action research). Authors call empirical data rare. **Evidence is thin; the rest is vendor case studies** |

Takeaways: semver is mostly honored now, and most breaks touch unused code, so *real* break rates are lower than folklore. Bots shrink lag but are met with suspicion, and "tests pass" under-detects breaks. This matches the first study's silent major-version-behind consumer.

## 4. Handoffs, templates and asking before building (L4, L5)

* **Clarifying is rare in practice.** An OSS feature-request study (arXiv 2507.13553; search summary only) says explicit clarification of incomplete requests is uncommon in issue trackers. Albayrak and Albayrak (2009; search summary: 251 engineers, 8 companies) report engineers facing incomplete requirements either ask or assume, and unchecked assumptions feed change requests and rework. Self-report surveys.
* **Distance and gaps.** Bjarnason and Sharp (search summaries only; Requirements Engineering 2017, 5 industrial case companies behind the 2019 EMSE paper) report that geographic, cognitive and semantic distances affect requirements communication and coordination. A "Gap Finder" prescribed practices; 7 of 9 judged practically relevant by practitioners. Case-study level, perception-based.
* **Knauss et al., Patterns of Continuous Requirements Clarification** (Requirements Engineering 2015; search summary only): one IBM case, a catalog of clarification patterns; late problems cause rework.
* **Templates.** Section 1 (issue templates) is the only quantitative support for a *required* template, observational and from OSS issue trackers rather than team handoffs.
* **Gap:** I found no study of a *written release-class handoff* (release class, version, who must act) and mismatched version expectations. The first study's one catch ([the pre-registration](pre-registration.md), §3.2) is our only datum.

## 5. LLM and agent developers (L1, L2, L4)

Everything here is benchmark work. Underspecification is mostly **synthetic**, which is also true of our tickets.

| Source | What I read | Strength and limits | Finding |
|---|---|---|---|
| SWE-bench Verified, OpenAI | Search summaries only (page returned 403) | Vendor annotation: 93 developers screened 1,699 samples, 500 kept | Underspecified issues were an explicit exclusion criterion; search summaries report GPT-4o at 33.2% on Verified and another scaffold doubling from 16%. Shows curation moves scores, but issue wording and test fixes were filtered together, so the issue-quality share is not separable |
| Aleithan et al., [SWE-Bench+](https://arxiv.org/abs/2410.06992) | Abstract via digest | Manual review of one agent's passing patches | **32.67% of successful patches had the solution given in the issue or comments**; 31.08% suspicious from weak tests; resolution fell 12.47% to 3.97% after filtering. A ticket that tells the answer inflates success; weak tests inflate it again |
| Vijayvargiya et al., [Ambig-SWE](https://arxiv.org/abs/2502.13069) (ICLR 2026) | Abstract via digest; method detail from a search summary | Underspecified variant of SWE-bench Verified, made by LLM summarization, with simulated users | Models struggle to tell well-specified from underspecified instructions; interaction improved results "up to 74%" (a maximum, not a typical gain). Prompting alone gave limited gains |
| Edwards and Schuster, [Ask or Assume?](https://arxiv.org/abs/2603.26233) | Abstract via digest | Same underspecified-Verified setup | A scaffold separating detection from execution reached 69.40% resolve and closed the gap to fully specified input; asks less on simple tasks |
| Vijayvargiya et al., [Asking What Matters](https://arxiv.org/abs/2604.14624) | Abstract via digest | Simulated users | Not all missing information matters equally; an 8B model matched a larger one with 41% fewer questions. Supports answering only from a key |
| Gloaguen et al., [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988) | Abstract via digest | 4 agents, SWE-bench tasks and a 138-task set | Context files did not generally raise success and raised cost over 20%; repo overviews did not help. Caution for "more structure is better" |
| Misleading hints ("Issue Misleading") in an automated-issue-solving failure taxonomy | Search-summary page only; the arXiv abstract I could open ([2509.13941](https://arxiv.org/abs/2509.13941)) does not mention it, and I could not confirm it is the same paper | Manual review of 150 failures | **Unverified.** Claims the most common failure subtype is agents following a wrong implementation hint from the issue. Treat as a lead, not evidence |
| Shi et al., [Distracted by irrelevant context](https://arxiv.org/abs/2302.00093) | Search summary only | Math benchmark, not coding | Irrelevant detail lowers accuracy; an instruction to ignore it helps. Only analogous to a decoy list |
| Liu et al., [Failures in automated issue solving](https://arxiv.org/abs/2509.13941) | Abstract via digest | 150 failures, SWE-bench Verified | Agentic failures mostly flawed reasoning and "cognitive deadlocks" |

**Missing dependents:** a search for a benchmark measuring call-site recall after a breaking change found none. Closest are BUMP (571 breaking Java updates from 153 projects), Byam and GitChameleon, which check compile, tests or API hit rate, not recall of dependents (search summaries only). Our scored "consumers missed" measure is novel relative to what I found.

## Claims we can test

| # | Claim | Side / source quality | Lever | Prediction | Prereg already covers it? |
|---|---|---|---|---|---|
| 1 | Structured tickets and templates shorten resolution and reduce reopenings | for; observational (issue templates), practitioner | L1 | 5, 6 | Partly: predictions concern exploration and rework; "reopened PRs" is scored |
| 2 | More instruction text does not help and raises cost | against; agent benchmark (AGENTS.md) | L1 | none | **No**: no prediction; tokens are recorded but not a headline outcome |
| 3 | Acceptance checks cut rework | for; opinion and perception (BDD) | L1 | 6 | Yes, but only if checks can fail (see claim 4) |
| 4 | Weak tests make results look better than they are | agent benchmark (SWE-bench+, Hejderup) | L1, scoring | none | **No**: acceptance script strength is not checked |
| 5 | A ticket that contains the answer inflates success | agent benchmark (SWE-bench+) | L1, L2 | none | Partly: complete list is covered; "answer in the ticket" is not separated |
| 6 | Smaller batches and ordered breakdown cut lead time and risk | for; DORA assertion; WIP case study mixed | L3 | none | Design only (L3 exists), no prediction; the first study found splitting did not help |
| 7 | A complete dependent list or catalog reduces misses | for; weak, mostly vendor; code search at Google | L2 | 1, 2 | Yes |
| 8 | Stale documentation is common | measured (Tan et al.) | L2 | 2 | Yes (stale catalog level) |
| 9 | Readers trust stale docs and are misled | no direct study found; agent analogy only | L2 | 2, 3 | Yes, but our own result will be one of few data points |
| 10 | Agents follow wrong hints | agent studies, partly unverified (MIRAGE-Bench, CodeCrash from snippets) | L2 decoy | 3 | Yes (decoy list), but not "wrong implementation hint" |
| 11 | Real breaking changes hit few consumers; most breaks touch unused code | observational (Ochoa) | change type | 8 | **No**: all three change types hit all consumers |
| 12 | Green CI after an update under-detects breaks | observational (Hejderup) | L6, scoring | none | Partly: post-merge breaks scored; no "CI green but break" cell |
| 13 | Semver, deprecation windows, bots, contracts reduce coordination cost | opinion, thin (Pact) | none | none | **No**: no release-mechanism lever |
| 14 | Asking helps when the ticket is truly underspecified; agents ask poorly | agent benchmark (Ambig-SWE, Ask or Assume) | L4 | none | Partly: L4 exists and questions counted, no prediction, no well-specified control |
| 15 | A required handoff template reduces mismatches | for; templates observational; gap studies perception-based | L5 | 7 | Yes |
| 16 | Layout (not process) governs deterministic measures | prior study; no outside source | none | 4 | Yes |
| 17 | Congruence and coordination effects are small or contested | observational, null result (Mauerer) | all | none | Partly: the 20% threshold and the "per outcome" reporting guard against over-claiming |

## Suggested additions to the prereg

Suggestions only. None has been applied.

1. **L2 or L1 level "ticket includes a wrong implementation hint."** Differs from a decoy consumer list: it tests following bad advice. Evidence: agent-failure taxonomy (unverified), CodeCrash/MIRAGE-Bench (snippets only). Add to the harm check.
2. **Solution-leakage control.** Add a level, or at least a scored flag, where the ticket names the exact edits. SWE-bench+ shows a third of agent "successes" came from this. Without it, structured-per-repository tasks (L1) and complete lists (L2) may look good only because they give the answer.
3. **Test-strength check on the acceptance script.** Run a mutation or seeded-fault pass (a consumer deliberately left unmigrated) to show the script can fail. Hejderup suggests tests miss many injected breaks.
4. **Over-specification cost outcome.** Report tokens, steps and clones per level of L1, with a prediction such as "acceptance checks add cost without cutting misses in the monorepo." The AGENTS.md result gives a reason to expect it. Prediction 5 only covers the multi-repo gain.
5. **A fourth change type: breaking change that does not touch one consumer.** Ochoa finds most breaks hit few clients; this tests false alarms and over-editing, and whether a catalog causes needless work.
6. **L4 refinements.** Add a well-specified control (does the agent ask needlessly?) and score whether it asks *when it should*, plus whether it states assumptions. A prediction for L4 is missing: "clarification helps only when the ticket omits the hidden consumer."
7. **Release-mechanism lever (L7).** Levels: none; deprecation shim kept for one version; consumer-driven contract check; automated PR to consumers (Renovate-style). The current plan has handoff (L5) but not the mechanisms practitioners use to avoid it. Pact-style evidence is thin, so this would be exploratory.
8. **Catalog trust measurement.** Record whether the agent verified catalog output with a search or grep before acting; this separates "trusted the stale entry" from "could not check." Also vary stale severity (one entry missing vs several wrong) to see whether any threshold exists.
9. **Noisy-ticket level for realism.** Real reports lack repro steps (Bettenburg) and generated tickets are cleaner. A script can degrade tickets Ambig-SWE-style (drop fields, vague wording). The prereg's limits section already admits this; this would reduce it.
10. **State WIP and queueing as out of scope.** The Kanban evidence is about concurrent work, which single-ticket runs cannot test. Add one line to "Out of scope" so the omission is deliberate.
11. **Power note.** Published effects are small or null (Mauerer; Ochoa). If the pilot shows spread near the 20% threshold, say in advance which extra replicates will be added, as the prereg already begins to do.

Related: [the pre-registration](pre-registration.md), monorepo vs multirepo evidence, [the first study](https://dlockamy.com/posts/2026/11/05/testing-the-monorepo-argument/).
