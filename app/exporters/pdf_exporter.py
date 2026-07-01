from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def export_pdf(report, output_file):

    doc = SimpleDocTemplate(output_file)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            report["title"],
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 12)
    )

    for section in report["sections"]:

        story.append(
            Paragraph(
                section["heading"],
                styles["Heading1"]
            )
        )

        story.append(
            Paragraph(
                section["content"],
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 12)
        )

    doc.build(story)