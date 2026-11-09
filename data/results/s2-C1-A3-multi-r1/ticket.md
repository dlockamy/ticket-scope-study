# PLAT-101: Customers can reach the billing portal

Type: Feature (with sub-tasks)   Priority: Medium   Assignee: you

## Description
Customers need a way to get from the billing component to the billing portal.

## Sub-tasks
- **PLAT-101-1** — repository: libs-shared-contracts (repository)
  Add the billing portal address to the shared configuration: `billingPortalUrl` = `https://homelab.local/billing/portal`. This is an additive, non-breaking change. Make it available to the apps that consume the shared configuration, following the team's release rules.
- **PLAT-101-2** — repository: apps-sub-route-billing (repository) — depends on PLAT-101-1
  In the billing component, add a link with the text "Manage billing" below the status line. Its address must come from the shared configuration's `billingPortalUrl`. Ship it.

## Acceptance criteria
- The billing component shows a link with the text "Manage billing" pointing at https://homelab.local/billing/portal.
- The address is defined in the shared configuration, not hardcoded in the billing app.

Definition of done: the change is live (merged and deployed through the normal pipelines).
