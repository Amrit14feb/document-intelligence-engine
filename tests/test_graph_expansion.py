from app.retrieval.graph_expansion import expand_entities


entities = [
    "UFSC",
    "FPGA"
]

expanded = expand_entities(
    entities,
    hops=1
)

print("\nEXPANDED ENTITIES\n")

for entity in expanded:

    print(entity)