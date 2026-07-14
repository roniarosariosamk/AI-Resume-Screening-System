from .llm import get_llm


def generate_interview_questions(summary, skills, job_description):

    llm = get_llm()

    prompt = f"""
You are an experienced technical interviewer.

Candidate Resume Summary:
{summary}

Candidate Skills:
{", ".join(skills)}

Job Description:
{job_description}

Generate exactly 5 interview questions.
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"❌ Gemini Error:\n\n{str(e)}"