# PLAT-103 (epic): Every app declares its owning team

Type: Epic   Priority: Medium   Assignee: you

## Description
Compliance needs every app to declare which team owns it. The shared contract validates apps at startup (`validateApp`).

This epic is split into child tickets. Work them in order. Show a child ticket with `st ticket <id>`; when its change is live, mark it done with `st ticket done <id>`. Close the epic with `st done` once every child ticket is done.

## Child tickets (in order)
1. PLAT-103-1: Make `validateApp` require an owner (shared contract) (repository: libs-shared-contracts (repository))
2. PLAT-103-2: The billing app passes its owner (repository: apps-sub-route-billing (repository)), depends on PLAT-103-1
3. PLAT-103-3: The core shell passes its owner (repository: apps-core-shell (repository)), depends on PLAT-103-1

## Acceptance criteria (epic)
- `validateApp` rejects apps without an `owner`.
- Every app that calls `validateApp` passes its owning team and still starts up.

Definition of done: the change is live (merged and deployed through the normal pipelines).
