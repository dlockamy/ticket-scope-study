# The ticket-scope study

Data, scripts and write-ups for a study of what decides whether a change that crosses repositories gets finished: the repository layout, or the ticket. AI agents played the developers and, in one phase, the reviewers. The blog post is at https://dlockamy.com/posts/2026/11/09/repo-or-ticket/ and the full report is at https://dlockamy.com/studies/ticket-scope/.

**Status: first report.** The numbers were re-checked against the raw data on 7 November 2026. No outside reader has read it yet. A human review round has not been run.

| Folder | What is in it |
|---|---|
| `report/` | The full report (markdown) |
| `docs/` | The pre-registration (written before the first run), the run log (each prediction as written before its phase, with outcomes), the outside-sources survey |
| `data/` | The harness scripts, ticket generator, scorer, analysis scripts and the per-run results (see `data/README.md`) |
| `figures/` | The three figures (SVG and PNG) and their captions and sources |
| `verification/` | Scripts that recompute the report's headline numbers from the raw results, their output, and the check of the 12 incomplete changes the report discusses |

**What is not here.** The human review kit's cases are not published, so that people who take part are not told what to look for.

**A note on the data.** Absolute home-directory paths in two log files were replaced with `/home/user/` before publication. Nothing else was changed. The e-mail addresses in the data are fake `study.local` addresses.

**Limits.** AI agents, not people; one small system of three apps and one shared library; five runs per ticket type; the same family of AI tools built the tests and played the developers. Section 6 of the report lists these and what was not tested.

**Licence.** Source code is Apache-2.0 (`LICENSE-APACHE`). The report, documents, figures and data are CC-BY-4.0 (`LICENSE-CC-BY-4.0`). `LICENSE` says which files fall under which.

*Parts of this repository were designed, written and tested with AI tools. A person reviews what is merged and is responsible for it. AI-assisted commits carry an `Assisted-by:` line.*
