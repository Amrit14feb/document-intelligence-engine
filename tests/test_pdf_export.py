from app.intelligence.structured_report_generator import (
    generate_structured_report
)

from app.exporters.pdf_exporter import (
    export_pdf
)

report = generate_structured_report()

export_pdf(
    report,
    "technical_report.pdf"
)

print("PDF Saved")