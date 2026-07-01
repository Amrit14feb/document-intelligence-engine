from app.intelligence.structured_report_generator import generate_structured_report
from app.exporters.docx_exporter import export_report

report = generate_structured_report()

export_report(
    report,
    "technical_report.docx"
)

print("Saved")