import os

from src.jd_parser import extract_job_description
from src.embeddings import load_embedding_model
from src.skill_matcher import extract_skills


def process_job_description(job_description):

    os.makedirs(
        "data/job_description",
        exist_ok=True
    )

    jd_path = os.path.join(
        "data/job_description",
        job_description.name
    )

    with open(jd_path, "wb") as f:
        f.write(job_description.getbuffer())

    jd_text = extract_job_description(jd_path)

    embedding_model = load_embedding_model()

    jd_embedding = embedding_model.embed_query(
        jd_text
    )

    jd_skills = extract_skills(
        jd_text
    )

    return (
        jd_text,
        jd_embedding,
        jd_skills
    )