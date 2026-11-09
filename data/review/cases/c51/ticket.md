# PLAT-103: Every app declares its owning team

Type: Feature request   Priority: Medium   Assignee: you

## Request
Compliance needs every app to declare which team owns it. The shared contract's `validateApp` should refuse apps that do not declare an `owner` (throw an error if it is missing or empty), and every app that calls `validateApp` must pass its owning team, as recorded in that app's `package.json` (`team`). Make sure nothing breaks.

## Acceptance criteria
- `validateApp` rejects apps without an `owner`.
- Every app that calls `validateApp` passes its owning team and still starts up.

(No breakdown has been done. Decide where the work belongs and record your sub-tasks with `st task add` before you start.)

Definition of done: the change is live (merged and deployed through the normal pipelines).
