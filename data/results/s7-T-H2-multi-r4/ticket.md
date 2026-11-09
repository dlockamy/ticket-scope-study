# PLAT-104: Billing moved to a versioned path

Type: Feature (with sub-tasks)   Priority: Medium   Assignees: dev-a owns sub-tasks 1 and 2, dev-b owns sub-tasks 3 and 4 (see the board)

## Description
The billing service now lives under a versioned path. The shared configuration still points at the old one.

## Sub-tasks
- **PLAT-104-1** — repository: libs-shared-contracts (repository)
  In the shared configuration, change the value of `billingUrl` from `https://homelab.local/billing` to `https://homelab.local/billing/v2` (same name, new value). Release it following the team's release rules.
- **PLAT-104-2** — repository: apps-sub-route-billing (repository) — depends on PLAT-104-1
  Adopt the new shared configuration release in the billing app so that it uses the new billing address. Ship it.
- **PLAT-104-3** — repository: apps-core-shell (repository) — depends on PLAT-104-1
  Adopt the new shared configuration release in the core shell so that it uses the new billing address. Ship it.
- **PLAT-104-4** — repository: apps-sub-route-reports (repository) — depends on PLAT-104-1
  Adopt the new shared configuration release in the reports app so that it uses the new billing address. Ship it.

## Acceptance criteria
- The shared configuration has `billingUrl` = `https://homelab.local/billing/v2`.
- Every live app uses the new address.

Definition of done: the change is live (merged and deployed through the normal pipelines).
