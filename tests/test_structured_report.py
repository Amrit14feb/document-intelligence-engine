from app.intelligence.structured_report_generator import (
    generate_structured_report
)

report = generate_structured_report()

print("\nTITLE\n")

print(
    report["title"]
)

print("\nSECTIONS\n")

for section in report["sections"]:

    print(
        section["heading"]
    )