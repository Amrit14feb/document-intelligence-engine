import json

with open(
    "data/knowledge/relationships.json",
    "r",
    encoding="utf-8"
) as f:
    relationships = json.load(f)

entities = set()

for rel in relationships:
    entities.add(rel["source"])
    entities.add(rel["target"])

print("\nGRAPH STATS\n")
print("Relationships:", len(relationships))
print("Unique Entities:", len(entities))