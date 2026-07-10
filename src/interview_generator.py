from .llm import load_llm

llm = load_llm()


def generate_interview_questions(summary, skills, job_description):

    print("Function Started")

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

    print("Prompt Created")

    response = llm.invoke(prompt)

    print("LLM Response Received")
    print(response)

    return response.content