# PLAT-104: Billing moved to a versioned path

Type: Feature (with sub-tasks)   Priority: Medium   Assignees: dev-a owns sub-tasks 1 and 2, dev-b owns sub-tasks 3 and 4 (see the board)

## Description
The billing service now lives under a versioned path. The shared configuration still points at the old one.

## Sub-tasks
- **PLAT-104-1** — repository: homelab-mfe-monorepo, libs/shared-contracts
  In the shared configuration, change the value of `billingUrl` from `https://homelab.local/billing` to `https://homelab.local/billing/v2` (same name, new value). Release it following the team's release rules.
- **PLAT-104-2** — repository: homelab-mfe-monorepo, apps/sub-route-billing — depends on PLAT-104-1
  Adopt the new shared configuration release in the billing app so that it uses the new billing address. Ship it.
- **PLAT-104-3** — repository: homelab-mfe-monorepo, apps/core-shell — depends on PLAT-104-1
  Adopt the new shared configuration release in the core shell so that it uses the new billing address. Ship it.
- **PLAT-104-4** — repository: homelab-mfe-monorepo, apps/sub-route-reports — depends on PLAT-104-1
  Adopt the new shared configuration release in the reports app so that it uses the new billing address. Ship it.

## Acceptance criteria
- The shared configuration has `billingUrl` = `https://homelab.local/billing/v2`.
- Every live app uses the new address.

Definition of done: the change is live (merged and deployed through the normal pipelines).
