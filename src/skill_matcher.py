import re

# Common technical skills
SKILLS = [
    "Python",
    "Java",
    "C++",
    "C",
    "JavaScript",
    "TypeScript",
    "React",
    "Angular",
    "Vue",
    "Node.js",
    "Express",
    "Django",
    "Flask",
    "FastAPI",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "SQLite",
    "Oracle",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Science",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "NLP",
    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Linux",
    "HTML",
    "CSS",
    "REST API",
    "REST",
    "GraphQL",
    "Power BI",
    "Excel"
]


def extract_skills(text):
    """
    Extract technical skills from text.
    """

    found_skills = []

    text = text.lower()

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(list(set(found_skills)))

def compare_skills(jd_skills, resume_skills):
    """
    Compare Job Description skills with Resume skills.
    Returns matched and missing skills.
    """

    jd_set = set(jd_skills)
    resume_set = set(resume_skills)

    matched = sorted(list(jd_set & resume_set))
    missing = sorted(list(jd_set - resume_set))

    return matched, missing

def calculate_ats_score(jd_skills, matched_skills):
    """
    Calculate ATS Match Percentage.
    """

    if len(jd_skills) == 0:
        return 0

    score = (len(matched_skills) / len(jd_skills)) * 100

    return round(score, 2)

def get_recommendation(score):
    """
    Return recommendation based on ATS score.
    """

    if score >= 90:
        return "🟢 Highly Recommended"

    elif score >= 70:
        return "🟡 Recommended"

    elif score >= 50:
        return "🟠 Consider for Interview"

    else:
        return "🔴 Needs Skill Improvement"