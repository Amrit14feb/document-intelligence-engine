import json


with open(
    "data/knowledge/relationships.json",
    "r",
    encoding="utf-8"
) as f:
    relationships = json.load(f)


ENTITY_SET = set()

for rel in relationships:

    ENTITY_SET.add(rel["source"])
    ENTITY_SET.add(rel["target"])


# -----------------------------------------
# MANUAL ALIASES
# -----------------------------------------

ALIASES = {

    "satoc": "Satellite-on-a-Chip",

    "satellite on a chip": "Satellite-on-a-Chip",

    "satellite-on-a-chip": "Satellite-on-a-Chip",

    "spacelab": "SpaceLab",

    "floripasat": "FloripaSat-1",

    "riscv": "RISC-V",

    "risc-v": "RISC-V",

    "obdh": "OBDH/OBC modules",

    "leon3": "LEON3 processor",

    "ppgeel": "PPGEEL/UFSC"
}


def detect_entities(question):

    question_lower = question.lower()

    detected = []


    # -------------------------------------
    # DIRECT ENTITY MATCH
    # -------------------------------------

    for entity in ENTITY_SET:

        if entity.lower() in question_lower:

            detected.append(entity)


    # -------------------------------------
    # ALIAS MATCH
    # -------------------------------------

    for alias, real_entity in ALIASES.items():

        if alias in question_lower:

            detected.append(real_entity)


    return list(set(detected))