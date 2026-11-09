#!/usr/bin/env python3
"""Scripted requester for the clarification lever (L4). Answers come only from key.json; it never volunteers
the list of consumers or any hint beyond what the key holds. usage: responder.py key.json "<question>" """
import json, re, sys
key = json.load(open(sys.argv[1])); q = sys.argv[2].lower()
for rule in key.get("rules", []):
    if any(re.search(p, q) for p in rule["match"]):
        print(rule["answer"]); sys.exit(0)
print(key.get("default", "I don't have more detail than what is in the ticket. Use your judgement."))
