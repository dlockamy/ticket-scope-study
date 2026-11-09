# PLAT-103: Every app declares its owning team

Type: Feature (with sub-tasks)   Priority: Medium   Assignee: you

## Description
Compliance needs every app to declare which team owns it. The shared contract validates apps at startup (`validateApp`).

## Sub-tasks
- **PLAT-103-1** — repository: libs-shared-contracts (repository)
  Make `validateApp` reject apps that do not declare an `owner`: throw an error if `owner` is missing or empty. This is a breaking change for consumers; release it following the team's release rules.
- **PLAT-103-2** — repository: apps-sub-route-billing (repository) — depends on PLAT-103-1
  Make the billing app pass its `owner` to `validateApp`: the owning team, as recorded in the app's `package.json` (`team`). Adopt the new shared configuration release and ship it.
- **PLAT-103-3** — repository: apps-sub-route-reports (repository) — depends on PLAT-103-1
  Make the reports app pass its `owner` to `validateApp`: the owning team, as recorded in the app's `package.json` (`team`). Adopt the new shared configuration release and ship it.

## Acceptance criteria
- `validateApp` rejects apps without an `owner`.
- Every app that calls `validateApp` passes its owning team and still starts up.

Definition of done: the change is live (merged and deployed through the normal pipelines).
