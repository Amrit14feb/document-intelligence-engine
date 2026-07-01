import json
from collections import Counter

with open(
    "data/knowledge/relationships_cleaned.json",
    "r",
    encoding="utf-8"
) as f:
    relationships = json.load(f)

source_counter = Counter()
target_counter = Counter()

for rel in relationships:

    source_counter[rel["source"]] += 1
    target_counter[rel["target"]] += 1

print("\nTOP SOURCES\n")

for entity, count in source_counter.most_common(30):

    print(f"{count:3} | {entity}")

print("\nTOP TARGETS\n")

for entity, count in target_counter.most_common(30):

    print(f"{count:3} | {entity}")