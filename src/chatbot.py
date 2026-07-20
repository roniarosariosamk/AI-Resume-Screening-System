from .embeddings import load_embedding_model
from .retriever import load_vector_store, retrieve_documents
from .llm import get_llm
from .prompts import prompt

try:
    from google.genai.errors import ServerError, ClientError
except ImportError:
    ServerError = Exception
    ClientError = Exception


def ask_question(question):
    """
    Ask questions about uploaded resumes using RAG.
    """

    try:
        # Load embedding model
        embedding = load_embedding_model()

        # Load FAISS vector store
        db = load_vector_store(embedding)

        # Load Gemini
        llm = get_llm()

        # Retrieve relevant documents
        docs = retrieve_documents(
            db,
            question,
            k=3
        )

        if not docs:
            return """
❌ No relevant resume information found.

Try asking another question.
"""

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        chain = prompt | llm

        response = chain.invoke(
            {
                "context": context,
                "question": question
            }
        )

        return response.content

    except ServerError as e:

        return f"""
❌ Gemini Server Error

Google's Gemini servers are currently busy.

Possible reasons:

• High traffic on Gemini
• Temporary server outage
• Internal Google server issue

Please wait a few seconds and try again.

Technical Details:

{e}
"""

    except ClientError as e:

        error_text = str(e)

        if "429" in error_text or "RESOURCEEXHAUSTED" in error_text:

            return """
❌ Gemini API Quota Exceeded

Your Gemini API has reached its usage limit.

Solutions:

• Wait for quota reset
• Generate a new API key
• Enable billing
• Upgrade Gemini plan
"""

        if "503" in error_text or "UNAVAILABLE" in error_text:

            return """
❌ Gemini Model Busy

The Gemini model is currently experiencing high demand.

Please try again after a few seconds.
"""

        return f"""
❌ Gemini Error

{error_text}
"""

    except Exception as e:

        return f"""
❌ Unexpected Error

{e}
"""