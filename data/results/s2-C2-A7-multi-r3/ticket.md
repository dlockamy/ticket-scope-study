# PLAT-102: Rename the misnamed billing setting

Type: Feature (with sub-tasks)   Priority: Medium   Assignee: you

## Description
`billingUrl` in the shared configuration is misnamed: it is the billing API endpoint, not a web page address.

## Sub-tasks
- **PLAT-102-1** — repository: libs-shared-contracts (repository)
  Rename `billingUrl` to `billingEndpoint` in the shared configuration (same value). This is a breaking change for consumers; release it following the team's release rules.
  Check: the shared configuration exports `billingEndpoint` and no longer `billingUrl`; the release version follows the team's rules.
- **PLAT-102-2** — repository: apps-sub-route-billing (repository) — depends on PLAT-102-1
  Update the billing app to use `billingEndpoint` everywhere and adopt the new shared configuration release. Ship it.
  Check: `grep -rn billingUrl` in this app returns nothing; the build passes; after CD, the live bundle no longer contains `billingUrl`.
- **PLAT-102-3** — repository: apps-core-shell (repository) — depends on PLAT-102-1
  Update the core shell to use `billingEndpoint` everywhere and adopt the new shared configuration release. Ship it.
  Check: `grep -rn billingUrl` in this app returns nothing; the build passes; after CD, the live bundle no longer contains `billingUrl`.

## Acceptance criteria
- No reference to `billingUrl` remains in the shared configuration or in any app that used it.
- Every live app still starts up.

Definition of done: the change is live (merged and deployed through the normal pipelines).
