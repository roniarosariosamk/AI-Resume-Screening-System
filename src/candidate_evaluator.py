from .llm import load_llm

llm = load_llm()


def evaluate_candidate(summary, skills, job_description):
    """
    Generate an AI evaluation of the candidate.
    """

    prompt = f"""
You are an experienced HR Manager.

Candidate Resume Summary:
{summary}

Candidate Skills:
{", ".join(skills)}

Job Description:
{job_description}

Evaluate the candidate based on:

1. Technical Skills (Rating out of 5)
2. Communication Skills (Rating out of 5)
3. Problem Solving (Rating out of 5)
4. Project Experience (Rating out of 5)

Also provide:

- Overall Score out of 10
- Strengths
- Weaknesses
- Final Recommendation

Keep the response professional and well formatted.
"""

    response = llm.invoke(prompt)

    return response.content