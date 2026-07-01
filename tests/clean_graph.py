import json

with open(
    "data/knowledge/relationships_cleaned.json",
    "r",
    encoding="utf-8"
) as f:
    relationships = json.load(f)

with open(
    "data/knowledge/entity_blacklist.json",
    "r",
    encoding="utf-8"
) as f:
    blacklist = set(json.load(f))

cleaned = []

for rel in relationships:

    source = rel["source"]
    target = rel["target"]

    if source in blacklist:
        continue

    if target in blacklist:
        continue

    cleaned.append(rel)

print("Before:", len(relationships))
print("After :", len(cleaned))

with open(
    "data/knowledge/relationships_v2.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        cleaned,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nSaved:")
print("data/knowledge/relationships_v2.json")