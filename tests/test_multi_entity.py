from app.retrieval.multi_entity_detector import detect_entities

print(
    detect_entities(
        "Tell me about UFSC and SpaceLab"
    )
)

print(
    detect_entities(
        "How are FPGA and UFSC connected?"
    )
)