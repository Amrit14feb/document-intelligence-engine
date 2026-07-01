from app.retrieval.entity_detector import detect_entity


print(
    detect_entity(
        "Tell me about SpaceLab"
    )
)

print(
    detect_entity(
        "Explain UFSC"
    )
)

print(
    detect_entity(
        "What is FPGA?"
    )
)