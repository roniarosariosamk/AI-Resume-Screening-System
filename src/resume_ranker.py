# ----------------------------------------------------
# Resume Ranker
# ----------------------------------------------------

from sklearn.metrics.pairwise import cosine_similarity


def rank_resumes(jd_embedding, resume_embeddings):
    """
    Rank resumes using the highest similarity score
    across all chunks belonging to the same resume.
    """

    resume_scores = {}

    for resume in resume_embeddings:

        similarity = cosine_similarity(
            [jd_embedding],
            [resume["embedding"]]
        )[0][0]

        resume_name = resume["name"]

        # Keep only the best score for each resume
        if resume_name not in resume_scores:
            resume_scores[resume_name] = similarity
        else:
            resume_scores[resume_name] = max(
                resume_scores[resume_name],
                similarity
            )

    ranking = []

    for name, score in resume_scores.items():

        ranking.append({
            "name": name,
            "score": float(score)
        })

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranking