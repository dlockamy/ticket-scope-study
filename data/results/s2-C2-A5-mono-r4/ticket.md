# PLAT-102: Rename the misnamed billing setting

Type: Feature request   Priority: Medium   Assignee: you

## Request
The setting called `billingUrl` in our shared configuration is misnamed: it is the billing API endpoint, not a web page address. We want it called `billingEndpoint` (same value) and every app that uses it should use the new name. Make sure nothing breaks.

## Acceptance criteria
- No reference to `billingUrl` remains in the shared configuration or in any app that used it.
- Every live app still starts up.

(No breakdown has been done. Decide where the work belongs and record your sub-tasks with `st task add` before you start.)

Definition of done: the change is live (merged and deployed through the normal pipelines).
