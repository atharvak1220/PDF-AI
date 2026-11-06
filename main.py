
from src.ask_naive import ask_question


def main():
    print("\nPDF loaded successfully!")
    print("Ask questions about your document.")
    print("Press Ctrl+C or Ctrl+D to exit.\n")

    while True:
        try:
            question = input("You: ")
            if not question.strip():
                continue

            print(f"\nGemini: {ask_question(question)}\n")
        except (EOFError, KeyboardInterrupt):
            print("\nConversation ended.")
            break
        except RuntimeError as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()
