import json

with open(
    "data/knowledge/relationships.json",
    "r",
    encoding="utf-8"
) as f:

    relationships = json.load(f)

print("\nSEARCHING FPGA...\n")

found = False

for rel in relationships:

    text = str(rel)

    if "fpga" in text.lower():

        found = True
        print(rel)
        print()

if not found:

    print("NO FPGA RELATIONSHIPS FOUND")