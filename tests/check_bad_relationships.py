import json

with open(
    "data/knowledge/relationships.json",
    "r",
    encoding="utf-8"
) as f:
    relationships = json.load(f)

for rel in relationships:

    source = rel["source"]
    target = rel["target"]

    if len(source) > 60 or len(target) > 60:
        print(rel)

    if "research" in target.lower():
        print(rel)

    if "same_day" in target.lower():
        print(rel)

    if "december" in target.lower():
        print(rel)