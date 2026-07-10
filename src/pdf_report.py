from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
    filename,
    candidate_name,
    ats_score,
    matched_skills,
    missing_skills,
    recommendation,
    evaluation
):
    """
    Generate ATS PDF Report.
    """

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>Resume Screening Report</b>", styles["Title"])
    )

    story.append(
        Paragraph(f"<b>Candidate:</b> {candidate_name}", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>ATS Score:</b> {ats_score:.2f}%", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Recommendation:</b> {recommendation}", styles["Normal"])
    )

    story.append(
        Paragraph("<b>Matched Skills</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(matched_skills, styles["BodyText"])
    )

    story.append(
        Paragraph("<b>Missing Skills</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(missing_skills, styles["BodyText"])
    )

    story.append(
        Paragraph("<b>AI Evaluation</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(evaluation.replace("\n", "<br/>"), styles["BodyText"])
    )

    doc.build(story)

    return filename