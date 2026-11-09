#!/usr/bin/env python3
"""Organization compliance check used by the B2 arm: every app that calls validateApp must pass an owner. Scans main of each app repo."""
import re, subprocess, sys
topo = sys.argv[1]
if topo == 'mono':
    apps = {'core-shell': ('/tmp/study/mono', 'apps/core-shell/src/config.js'), 'sub-route-billing': ('/tmp/study/mono', 'apps/sub-route-billing/src/main.js'), 'sub-route-reports': ('/tmp/study/mono', 'apps/sub-route-reports/src/main.js')}
else:
    apps = {'core-shell': ('/tmp/study/multi/apps-core-shell', 'src/config.js'), 'sub-route-billing': ('/tmp/study/multi/apps-sub-route-billing', 'src/main.js'), 'sub-route-reports': ('/tmp/study/multi/apps-sub-route-reports', 'src/main.js')}
bad = 0
print('Compliance check: apps that call validateApp must declare an owner (main branches)')
for name, (repo, path) in apps.items():
    try: src = subprocess.check_output(['git', '-C', repo, 'show', f'main:{path}'], text=True, stderr=subprocess.DEVNULL)
    except Exception: print(f'  SKIP {name}: cannot read'); continue
    calls = re.findall(r'validateApp\s*\(([^)]*)\)', src)
    calls = [c for c in calls if 'function' not in c]
    if not calls: print(f'  OK   {name}: no validateApp call'); continue
    if all(re.search(r'owner', c) for c in calls): print(f'  OK   {name}: declares an owner')
    else: print(f'  VIOLATION {name}: validateApp called without an owner'); bad += 1
print(f'{bad} violation(s)')
sys.exit(1 if bad else 0)
