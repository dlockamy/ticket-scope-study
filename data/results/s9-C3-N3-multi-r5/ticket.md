# PLAT-103: Every app declares its owning team

Type: Feature request   Priority: Medium   Assignee: you

## Request
Compliance needs every app to declare which team owns it. In `libs-config` (the shared configuration library), make `validateApp` reject apps that do not declare an `owner` (throw if it is missing or empty). This is a breaking change; release it following the team's release rules. Every app that calls `validateApp` must then pass its owning team, as recorded in the app's `package.json` (`team`).

## Acceptance criteria
- `validateApp` rejects apps without an `owner`.
- Every app that calls `validateApp` passes its owning team and still starts up.

(No breakdown has been done. Decide where the work belongs and record your sub-tasks with `st task add` before you start.)

Definition of done: the change is live (merged and deployed through the normal pipelines).
