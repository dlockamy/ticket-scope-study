#!/usr/bin/env python3
"""Ticket generator for the ticket-structure/process study (s2).

usage: gen.py <mono|multi> <C1|C2|C3> <A1..A7> <run-dir> [clarify]

Writes into <run-dir>: ticket.md, catalog.json (if the arm has a catalog), key.json (scripted requester),
brief.md fragments (extra.txt), and prints a JSON object of meta fields.

Ticket text is produced from templates only (no model involved) and is identical across layouts apart from
repository names. Every arm is a point in the lever space of monorepo-followup-ticket-process-prereg:

  arm  L1 ticket structure            L2 dependent information
  A1   open-ended                     none
  A2   structured per repository      partial list (the reports consumer is missing)
  A3   structured per repository      complete list
  A4   structured per repository      decoy list (names libs-platform-kit, which does not consume; omits reports)
  A5   open-ended                     catalog tool `st deps`, complete
  A6   open-ended                     catalog tool `st deps`, stale (reports missing)
  A7   structured + acceptance checks partial list (reports missing)
"""
import json, os, sys

topo, change, arm, rundir = sys.argv[1:5]
clarify = len(sys.argv) > 5 and sys.argv[5] == 'clarify'

ARMS = {
    'A1': dict(structure='open', lst='none', catalog='none', checks=False),
    'A2': dict(structure='structured', lst='partial', catalog='none', checks=False),
    'A3': dict(structure='structured', lst='complete', catalog='none', checks=False),
    'A4': dict(structure='structured', lst='decoy', catalog='none', checks=False),
    'A5': dict(structure='open', lst='none', catalog='complete', checks=False),
    'A6': dict(structure='open', lst='none', catalog='stale', checks=False),
    'A7': dict(structure='structured', lst='partial', catalog='none', checks=True),
    # phase 2 (C3 only): fixes for the structured-partial miss, and a different hidden consumer
    'B1': dict(structure='structured', lst='partial', catalog='none', checks=False, note='discover'),
    'B2': dict(structure='structured', lst='partial', catalog='none', checks=False, audit=True),
    'B3': dict(structure='structured', lst='partial', catalog='none', checks=False, clarify=True),
    'B4': dict(structure='structured', lst='partial', catalog='none', checks=False, note='caveat'),
    'A2s': dict(structure='structured', lst='partial_shell', catalog='none', checks=False),
    # phase 8: epic with ordered child tickets
    'E1': dict(structure='epic', lst='partial', catalog='none', checks=False, epic=True, verify=False),
    'E2': dict(structure='epic', lst='complete', catalog='none', checks=False, epic=True, verify=False),
    'E3': dict(structure='epic', lst='partial', catalog='none', checks=False, epic=True, verify=True),
    # phase 9: degraded open-ended tickets (C3 only)
    'N1': dict(structure='open', lst='none', catalog='none', checks=False, custom='terse'),
    'N2': dict(structure='open', lst='none', catalog='none', checks=False, custom='thread'),
    'N3': dict(structure='open', lst='none', catalog='none', checks=False, custom='stale'),
    'N2b': dict(structure='open', lst='none', catalog='none', checks=False, custom='thread2'),
}
a = ARMS[arm]
clarify = clarify or a.get('clarify', False)
HIDDEN = {'partial': 'reports', 'decoy': 'reports', 'partial_shell': 'shell'}.get(a['lst'])

LOC = {
    'mono': {'contracts': 'homelab-mfe-monorepo, libs/shared-contracts', 'shell': 'homelab-mfe-monorepo, apps/core-shell',
             'billing': 'homelab-mfe-monorepo, apps/sub-route-billing', 'reports': 'homelab-mfe-monorepo, apps/sub-route-reports',
             'platformkit': 'libs-platform-kit (own repository)'},
    'multi': {'contracts': 'libs-shared-contracts (repository)', 'shell': 'apps-core-shell (repository)',
              'billing': 'apps-sub-route-billing (repository)', 'reports': 'apps-sub-route-reports (repository)',
              'platformkit': 'libs-platform-kit (repository)'},
}[topo]
NAME = {'shell': 'core shell', 'billing': 'billing app', 'reports': 'reports app', 'platformkit': 'platform kit'}
DOD = "Definition of done: the change is live (merged and deployed through the normal pipelines)."

CHANGES = {
    'C1': dict(key='PLAT-101', title='Customers can reach the billing portal',
        desc='Customers need a way to get from the billing component to the billing portal.',
        contract="Add the billing portal address to the shared configuration: `billingPortalUrl` = `https://homelab.local/billing/portal`. This is an additive, non-breaking change. Make it available to the apps that consume the shared configuration, following the team's release rules.",
        consumer={'billing': "In the billing component, add a link with the text \"Manage billing\" below the status line. Its address must come from the shared configuration's `billingPortalUrl`. Ship it."},
        open_desc="As a customer, I want to be able to get from the billing component to the billing portal, so that I can manage my payment methods.\n\nNotes from product:\n- The portal address is environment configuration. It must live with the shared configuration that all our apps use, and must not be hardcoded in the billing app.\n- Portal address: https://homelab.local/billing/portal\n- Link text: \"Manage billing\"",
        accept=['The billing component shows a link with the text "Manage billing" pointing at https://homelab.local/billing/portal.', 'The address is defined in the shared configuration, not hardcoded in the billing app.'],
        users=['billing']),
    'C2': dict(key='PLAT-102', title='Rename the misnamed billing setting',
        desc='`billingUrl` in the shared configuration is misnamed: it is the billing API endpoint, not a web page address.',
        contract="Rename `billingUrl` to `billingEndpoint` in the shared configuration (same value). This is a breaking change for consumers; release it following the team's release rules.",
        consumer={k: f"Update the {NAME[k]} to use `billingEndpoint` everywhere and adopt the new shared configuration release. Ship it." for k in ('shell', 'billing', 'reports')} | {'platformkit': "Update the platform kit to read `billingEndpoint` instead of `billingUrl`, and adopt the new shared configuration release. Ship it."},
        open_desc="The setting called `billingUrl` in our shared configuration is misnamed: it is the billing API endpoint, not a web page address. We want it called `billingEndpoint` (same value) and every app that uses it should use the new name. Make sure nothing breaks.",
        accept=['No reference to `billingUrl` remains in the shared configuration or in any app that used it.', 'Every live app still starts up.'],
        checks={'contracts': "Check: the shared configuration exports `billingEndpoint` and no longer `billingUrl`; the release version follows the team's rules.",
                'app': "Check: `grep -rn billingUrl` in this app returns nothing; the build passes; after CD, the live bundle no longer contains `billingUrl`."},
        users=['shell', 'billing', 'reports']),
    'C3': dict(key='PLAT-103', title='Every app declares its owning team',
        desc='Compliance needs every app to declare which team owns it. The shared contract validates apps at startup (`validateApp`).',
        contract="Make `validateApp` reject apps that do not declare an `owner`: throw an error if `owner` is missing or empty. This is a breaking change for consumers; release it following the team's release rules.",
        consumer={k: f"Make the {NAME[k]} pass its `owner` to `validateApp`: the owning team, as recorded in the app's `package.json` (`team`). Adopt the new shared configuration release and ship it." for k in ('shell', 'billing', 'reports')} | {'platformkit': "Make the platform kit pass its `owner` to `validateApp`, and adopt the new shared configuration release. Ship it."},
        open_desc="Compliance needs every app to declare which team owns it. The shared contract's `validateApp` should refuse apps that do not declare an `owner` (throw an error if it is missing or empty), and every app that calls `validateApp` must pass its owning team, as recorded in that app's `package.json` (`team`). Make sure nothing breaks.",
        accept=['`validateApp` rejects apps without an `owner`.', 'Every app that calls `validateApp` passes its owning team and still starts up.'],
        checks={'contracts': "Check: `validateApp({name: 'x'})` throws and `validateApp({name: 'x', owner: 't'})` returns the app; the release version follows the team's rules.",
                'app': "Check: after CD, the app's bundle starts without throwing and its app record has `owner` set to the team from this app's `package.json`."},
        users=['shell', 'billing', 'reports']),
    'C4': dict(key='PLAT-104', title='Billing moved to a versioned path',
        desc='The billing service now lives under a versioned path. The shared configuration still points at the old one.',
        contract="In the shared configuration, change the value of `billingUrl` from `https://homelab.local/billing` to `https://homelab.local/billing/v2` (same name, new value). Release it following the team's release rules.",
        consumer={k: f"Adopt the new shared configuration release in the {NAME[k]} so that it uses the new billing address. Ship it." for k in ('shell', 'billing', 'reports')} | {'platformkit': "Adopt the new shared configuration release in the platform kit. Ship it."},
        open_desc="The billing service now lives under a versioned path. In our shared configuration, `billingUrl` should be `https://homelab.local/billing/v2` instead of `https://homelab.local/billing` (same name, new value), and every app that uses it should pick up the new address.",
        accept=['The shared configuration has `billingUrl` = `https://homelab.local/billing/v2`.', 'Every live app uses the new address.'],
        checks={'contracts': "Check: the shared configuration exports the new value; the release version follows the team's rules.", 'app': "Check: after CD, the live bundle contains the new address."},
        users=['shell', 'billing', 'reports']),
}
C = CHANGES[change]

def listed():
    """Consumers named in a structured ticket for this arm."""
    if change == 'C1':
        return ['billing'], []
    if a['lst'] == 'partial':
        return ['billing', 'shell'], []
    if a['lst'] == 'partial_shell':
        return ['billing', 'reports'], []
    if a['lst'] == 'complete':
        return ['billing', 'shell', 'reports'], []
    if a['lst'] == 'decoy':
        return ['billing', 'shell'], ['platformkit']
    return [], []

out = [f"# {C['key']}: {C['title']}", ""]
if a['structure'] == 'structured':
    cons, decoys = listed()
    desc = C['desc'] + (" The sub-tasks below cover the apps we know about. Others may also be affected." if a.get('note') == 'caveat' else "")
    out += ["Type: Feature (with sub-tasks)   Priority: Medium   Assignee: you", "", "## Description", desc, ""]
    if a.get('note') == 'discover':
        out += ["Before you start, find every app that uses `validateApp` (not only those below) and add a sub-task for each with `st task add`.", ""]
    out += ["## Sub-tasks"]
    n = 1
    out += [f"- **{C['key']}-{n}** — repository: {LOC['contracts']}", f"  {C['contract']}"]
    if a['checks'] and 'checks' in C: out += [f"  {C['checks']['contracts']}"]
    for k in cons + decoys:
        n += 1
        out += [f"- **{C['key']}-{n}** — repository: {LOC[k]} — depends on {C['key']}-1", f"  {C['consumer'][k]}"]
        if a['checks'] and 'checks' in C: out += [f"  {C['checks']['app']}"]
    out += ["", "## Acceptance criteria"] + [f"- {x}" for x in C['accept']] + (["- `st audit` reports no violations."] if a.get('audit') else [])
else:
    out += ["Type: Feature request   Priority: Medium   Assignee: you", "", "## Request", C['open_desc'], "", "## Acceptance criteria"] + [f"- {x}" for x in C['accept']]
    out += ["", "(No breakdown has been done. Decide where the work belongs and record your sub-tasks with `st task add` before you start.)"]
out += ["", DOD, ""]
open(f'{rundir}/ticket.md', 'w').write("\n".join(out))
CHILD_IDS = []
NOBREAK = "(No breakdown has been done. Decide where the work belongs and record your sub-tasks with `st task add` before you start.)"
if a.get('custom'):
    assert change == 'C3'
    K = C['key']
    if a['custom'] == 'terse':
        txt = f"# {K}: Owners for apps\n\nType: Task   Priority: Medium   Assignee: you\n\n`validateApp` should require an owner. Apps pass their team (it's in package.json). Release per team rules.\n\n{NOBREAK}\n\n{DOD}\n"
    elif a['custom'] in ('thread', 'thread2'):
        txt = f"""# {K}: Owners for apps (from the #platform thread)

Type: Task   Priority: Medium   Assignee: you

## Request (pasted from Slack)
> priya: did anyone look at why CI was slow on Tuesday? the docker pull step took forever
> sam: that was the registry mirror, ignore it
> lee (compliance): quick one from the audit. we need every app to say which team owns it, right now nothing enforces that
> lee: {'idea is validateApp should throw if there is no `owner`, and apps pass their team as the owner (the `team` field in their package.json)' if a['custom'] == 'thread2' else "idea is validateApp should throw if there's no owner, and apps pass their team, the one in their package.json `team`"}
> priya: that's breaking for anyone on the old version obviously
> sam: yeah so major. also can we stop using the fake bucket names in the readme, they confuse people
> lee: separate thing! can someone just pick this up? we need it before the audit on the 14th
> priya: I can't, I'm on the release train. someone from platform?
(that's you)

{NOBREAK}

{DOD}
"""
    else:
        old = 'libs/config' if topo == 'mono' else 'libs-config'
        txt = f"""# {K}: {C['title']}

Type: Feature request   Priority: Medium   Assignee: you

## Request
Compliance needs every app to declare which team owns it. In `{old}` (the shared configuration library), make `validateApp` reject apps that do not declare an `owner` (throw if it is missing or empty). This is a breaking change; release it following the team's release rules. Every app that calls `validateApp` must then pass its owning team, as recorded in the app's `package.json` (`team`).

## Acceptance criteria
""" + "\n".join(f"- {x}" for x in C['accept']) + f"\n\n{NOBREAK}\n\n{DOD}\n"
    open(f'{rundir}/ticket.md', 'w').write(txt)
if a.get('epic'):
    assert change == 'C3'
    K = C['key']; cons, decoys = listed(); os.makedirs(f'{rundir}/children', exist_ok=True)
    kids = [(f"{K}-1", f"Make `validateApp` require an owner (shared contract)", LOC['contracts'], C['contract'], None)]
    for i, k in enumerate(cons, 2):
        kids.append((f"{K}-{i}", f"The {NAME[k]} passes its owner", LOC[k], C['consumer'][k], f"{K}-1"))
    if a.get('verify'):
        kids.append((f"{K}-{len(kids)+1}", "Verify the epic", "all repositories", "Confirm that every app that calls `validateApp` has been updated to pass its owner, and fix or report any that has not.", f"{K}-1"))
    for cid, title, loc, text, dep in kids:
        open(f'{rundir}/children/{cid}.md', 'w').write(f"# {cid}: {title}\n\nType: Child ticket of {K}   Priority: Medium   Assignee: you\nRepository: {loc}" + (f"\nDepends on: {dep}" if dep else "") + f"\n\n{text}\n\nWhen this is live, run `st ticket done {cid}`.\n")
    CHILD_IDS = [x[0] for x in kids]
    lines = [f"# {K} (epic): {C['title']}", "", "Type: Epic   Priority: Medium   Assignee: you", "", "## Description", C['desc'], "",
             "This epic is split into child tickets. Work them in order. Show a child ticket with `st ticket <id>`; when its change is live, mark it done with `st ticket done <id>`. Close the epic with `st done` once every child ticket is done.", "", "## Child tickets (in order)"]
    for n, (cid, title, loc, text, dep) in enumerate(kids, 1): lines.append(f"{n}. {cid}: {title} (repository: {loc})" + (f", depends on {dep}" if dep else ""))
    lines += ["", "## Acceptance criteria (epic)"] + [f"- {x}" for x in C['accept']] + ["", DOD, ""]
    open(f'{rundir}/ticket.md', 'w').write("\n".join(lines))

# dependency catalog (arms A5, A6): consumers of @mfe/shared-contracts
if a['catalog'] != 'none':
    path = {'mono': {'shell': 'homelab-mfe-monorepo: apps/core-shell', 'billing': 'homelab-mfe-monorepo: apps/sub-route-billing', 'reports': 'homelab-mfe-monorepo: apps/sub-route-reports'},
            'multi': {'shell': 'apps-core-shell', 'billing': 'apps-sub-route-billing', 'reports': 'apps-sub-route-reports'}}[topo]
    cons = ['shell', 'billing', 'reports']
    if a['catalog'] == 'stale': cons = ['shell', 'billing']   # the newest consumer (reports) was never added
    cat = {'@mfe/shared-contracts': [path[k] for k in cons],
           '@studio/platform-kit': ['homelab-mfe-monorepo: apps/sub-route-billing' if topo == 'mono' else 'apps-sub-route-billing']}
    json.dump(cat, open(f'{rundir}/catalog.json', 'w'), indent=1)

# scripted requester (only used when the clarification lever is on)
key = {'rules': [
    {'match': ['consumer', 'depend', 'who uses', 'which (apps|repos|repositories)', 'affect', 'list of'],
     'answer': "I don't have a complete list of what uses it; that's why the ticket says what it says. Please check the code."},
    {'match': ['owner', 'team'], 'answer': "The owner is the owning team as recorded in each app's package.json."},
    {'match': ['semver', 'version', 'breaking', 'release', 'major', 'minor'], 'answer': "Follow the team's release rules in CONTRIBUTING.md."},
    {'match': ['value', 'name', 'same', 'rename'], 'answer': "Keep the values exactly as they are today; only what the ticket says changes."},
    {'match': ['deadline', 'urgent', 'when'], 'answer': "No fixed deadline; please just get it live properly."},
], 'default': "I don't have more detail than what is in the ticket. Use your judgement."}
json.dump(key, open(f'{rundir}/key.json', 'w'), indent=1)

extra = []
if a['catalog'] != 'none':
    extra.append("- `st deps <package>` shows the team's dependency catalog: which repositories depend on a package.")
if a.get('epic'):
    extra.append("- The ticket is an epic with ordered child tickets: `st ticket <id>` shows one, `st ticket done <id>` marks it done when it is live. The epic can be closed with `st done` only when every child ticket is done.")
if a.get('audit'):
    extra.append("- `st audit` runs the organization's compliance check across the main branch of every app repository.")
if clarify:
    extra.append("- `st ask \"<question>\"` lets you ask the person who wrote the ticket a clarifying question (at most 3).")
open(f'{rundir}/extra.txt', 'w').write("\n".join(extra))

cons, decoys = listed()
print(json.dumps(dict(structure=a['structure'], list=a['lst'], catalog=a['catalog'], checks=a['checks'], clarify=clarify,
                      listed=cons, decoys=decoys, hidden=HIDDEN, epic=bool(a.get('epic')), children=CHILD_IDS, custom=a.get('custom'), audit=bool(a.get('audit')), note=a.get('note'), users=C['users'], ticket_key=C['key'])))
