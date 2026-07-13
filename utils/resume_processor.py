import os

from src.parser import extract_text, generate_resume_summary

from src.skill_matcher import (
    extract_skills,
    compare_skills,
    calculate_ats_score,
    get_recommendation,

)


def process_resume(uploaded_file, jd_skills):

    os.makedirs("RESUME_FOLDER", exist_ok=True)

    pdf_path = os.path.join(
        "RESUME_FOLDER",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text(pdf_path)

    summary = generate_resume_summary(text)

    resume_skills = extract_skills(text)

    matched, missing = compare_skills(
        jd_skills,
        resume_skills
    )

    ats_score = calculate_ats_score(
        jd_skills,
        matched
    )

    recommendation = get_recommendation(
        ats_score
    )

    return (
        text,
        summary,
        resume_skills,
        matched,
        missing,
        ats_score,
        recommendation
    )