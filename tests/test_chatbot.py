import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from src.chatbot import ask_question


def main():

    print("=" * 70)
    print("RESUME RAG CHATBOT")
    print("=" * 70)

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        answer = ask_question(question)

        print("\nAnswer:")
        print("-" * 60)
        print(answer)


if __name__ == "__main__":
    main()