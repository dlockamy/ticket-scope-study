# PLAT-102: Rename the misnamed billing setting

Type: Feature (with sub-tasks)   Priority: Medium   Assignee: you

## Description
`billingUrl` in the shared configuration is misnamed: it is the billing API endpoint, not a web page address.

## Sub-tasks
- **PLAT-102-1** — repository: homelab-mfe-monorepo, libs/shared-contracts
  Rename `billingUrl` to `billingEndpoint` in the shared configuration (same value). This is a breaking change for consumers; release it following the team's release rules.
- **PLAT-102-2** — repository: homelab-mfe-monorepo, apps/sub-route-billing — depends on PLAT-102-1
  Update the billing app to use `billingEndpoint` everywhere and adopt the new shared configuration release. Ship it.
- **PLAT-102-3** — repository: homelab-mfe-monorepo, apps/core-shell — depends on PLAT-102-1
  Update the core shell to use `billingEndpoint` everywhere and adopt the new shared configuration release. Ship it.
- **PLAT-102-4** — repository: libs-platform-kit (own repository) — depends on PLAT-102-1
  Update the platform kit to read `billingEndpoint` instead of `billingUrl`, and adopt the new shared configuration release. Ship it.

## Acceptance criteria
- No reference to `billingUrl` remains in the shared configuration or in any app that used it.
- Every live app still starts up.

Definition of done: the change is live (merged and deployed through the normal pipelines).
