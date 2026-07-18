from .llm import get_llm
from .gemini_utils import extract_text
try:
    from google.genai.errors import ClientError
except ImportError:
    ClientError = Exception


def evaluate_candidate(summary, skills, job_description):
    """
    Generate an AI evaluation of the candidate.
    """

    llm = get_llm()

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

    try:
        response = llm.invoke(prompt)

        return extract_text(response)

        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):

            text = ""

            for item in content:

                if hasattr(item, "text"):
                    text += item.text + "\n"

                elif isinstance(item, dict):
                    text += item.get("text", "")

                else:
                    text += str(item)

            return text.strip()

        return str(content)

    except ClientError as e:

        error_text = str(e)

        if "RESOURCEEXHAUSTED" in error_text or "429" in error_text:
            return """
❌ Gemini API Quota Exceeded

Your Gemini API has reached its current usage limit.

Possible reasons:
• Daily free quota exhausted
• Requests per minute exceeded
• Token limit exceeded

Solutions:
• Wait until the quota resets
• Generate a new API key
• Enable billing in Google AI Studio
• Upgrade your Gemini plan

The candidate evaluation could not be generated at this time.
"""

        return f"Gemini API Error:\n\n{error_text}"

    except Exception as e:
        return f"Unexpected Error:\n\n{e}"