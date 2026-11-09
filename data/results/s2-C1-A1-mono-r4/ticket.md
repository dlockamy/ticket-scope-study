# PLAT-101: Customers can reach the billing portal

Type: Feature request   Priority: Medium   Assignee: you

## Request
As a customer, I want to be able to get from the billing component to the billing portal, so that I can manage my payment methods.

Notes from product:
- The portal address is environment configuration. It must live with the shared configuration that all our apps use, and must not be hardcoded in the billing app.
- Portal address: https://homelab.local/billing/portal
- Link text: "Manage billing"

## Acceptance criteria
- The billing component shows a link with the text "Manage billing" pointing at https://homelab.local/billing/portal.
- The address is defined in the shared configuration, not hardcoded in the billing app.

(No breakdown has been done. Decide where the work belongs and record your sub-tasks with `st task add` before you start.)

Definition of done: the change is live (merged and deployed through the normal pipelines).
