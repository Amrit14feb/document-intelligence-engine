import json

INPUT_FILE = "data/knowledge/relationships.json"
OUTPUT_FILE = "data/knowledge/relationships_cleaned.json"


BAD_TARGETS = {
    "research_field",
    "same_day_of_launch",
    "research and development",
    "research and development activities"
}


BAD_RELATIONS = {
    "co_author_of",
    "co-authored"
}


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    relationships = json.load(f)


cleaned = []

for rel in relationships:

    source = rel["source"]
    relation = rel["relationship"]
    target = rel["target"]

    if relation in BAD_RELATIONS:
        continue

    if target.lower() in BAD_TARGETS:
        continue

    if len(target) > 100:
        continue

    cleaned.append(rel)


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        cleaned,
        f,
        indent=4,
        ensure_ascii=False
    )


print("Before:", len(relationships))
print("After :", len(cleaned))