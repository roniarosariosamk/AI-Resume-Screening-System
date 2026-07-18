from .llm import get_llm
from .gemini_utils import extract_text


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

        return extract_text(response)

        content = response.content
    

        # Case 1 : Normal string
        if isinstance(content, str):
            return content

        # Case 2 : List returned by Gemini
        if isinstance(content, list):

            text = ""

            for item in content:

                # LangChain object
                if hasattr(item, "text"):
                    text += item.text + "\n"

                # Dictionary
                elif isinstance(item, dict):
                    text += item.get("text", "")

                else:
                    text += str(item)

            return text.strip()

        # Fallback
        return str(content)

    except Exception as e:
        # Catch all errors (specific SDK exception may not be available/imported)
        return f"❌ Gemini Error:\n\n{str(e)}"