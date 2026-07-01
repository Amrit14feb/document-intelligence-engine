import json


with open(
    "data/knowledge/entities.json",
    "r",
    encoding="utf-8"
) as f:

    entities = json.load(f)


ALL_ENTITIES = []

for category in entities:

    ALL_ENTITIES.extend(
        entities[category]
    )


ALIASES = {

    "satoc": "Satellite-on-a-Chip",

    "satellite on a chip": "Satellite-on-a-Chip",

    "satellite-on-a-chip": "Satellite-on-a-Chip",

    "spacelab": "SpaceLab",

    "ufsc": "UFSC",

    "fpga": "FPGA",

    "riscv": "RISC-V",

    "risc-v": "RISC-V",

    "floripasat": "FloripaSat-1",

    "leon3": "LEON3 processor",

    "ppgeel": "PPGEEL/UFSC",

    "obdh": "OBDH/OBC modules"
}


def detect_entities(question):

    question_lower = question.lower()

    found = []


    # ------------------------
    # Direct Entity Match
    # ------------------------

    for entity in ALL_ENTITIES:

        if entity.lower() in question_lower:

            found.append(entity)


    # ------------------------
    # Alias Match
    # ------------------------

    for alias, entity in ALIASES.items():

        if alias in question_lower:

            found.append(entity)


    return list(set(found))