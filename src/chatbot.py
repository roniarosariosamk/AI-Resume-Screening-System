from .embeddings import load_embedding_model
from .retriever import load_vector_store, retrieve_documents
from .llm import get_llm
from .prompts import prompt


def ask_question(question):

    # Load only when the function is called
    embedding = load_embedding_model()
    db = load_vector_store(embedding)
    llm = get_llm()

    docs = retrieve_documents(
        db,
        question,
        k=3
    )

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