# PLAT-103: Owners for apps (from the #platform thread)

Type: Task   Priority: Medium   Assignee: you

## Request (pasted from Slack)
> priya: did anyone look at why CI was slow on Tuesday? the docker pull step took forever
> sam: that was the registry mirror, ignore it
> lee (compliance): quick one from the audit. we need every app to say which team owns it, right now nothing enforces that
> lee: idea is validateApp should throw if there is no `owner`, and apps pass their team as the owner (the `team` field in their package.json)
> priya: that's breaking for anyone on the old version obviously
> sam: yeah so major. also can we stop using the fake bucket names in the readme, they confuse people
> lee: separate thing! can someone just pick this up? we need it before the audit on the 14th
> priya: I can't, I'm on the release train. someone from platform?
(that's you)

(No breakdown has been done. Decide where the work belongs and record your sub-tasks with `st task add` before you start.)

Definition of done: the change is live (merged and deployed through the normal pipelines).
