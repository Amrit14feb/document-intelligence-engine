import json
import os

from pyvis.network import Network


# =====================================
# LOAD KNOWLEDGE GRAPH
# =====================================

with open(
    "data/knowledge/knowledge_graph.json",
    "r",
    encoding="utf-8"
) as f:

    kg = json.load(f)


# =====================================
# CREATE NETWORK
# =====================================

net = Network(
    height="800px",
    width="100%",
    directed=True
)


# =====================================
# ADD RELATIONSHIPS
# =====================================

relationships = kg["relationships"]

for rel in relationships:

    source = rel["source"]
    target = rel["target"]
    relation = rel["relationship"]

    net.add_node(source, label=source)

    net.add_node(target, label=target)

    net.add_edge(
        source,
        target,
        label=relation
    )


# =====================================
# SAVE HTML
# =====================================

os.makedirs(
    "outputs",
    exist_ok=True
)

output_file = "outputs/knowledge_graph.html"

net.write_html(
    output_file,
    notebook=False
)

print("\n=================================")
print("GRAPH CREATED")
print(output_file)
print("=================================\n")