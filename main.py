
from pathlib import Path

from src.extract import extract_pdf
from src.ask_naive import ask_question


def main():
    project_root = Path(__file__).resolve().parent
    pdf_path = project_root / "data" / "Project.pdf"

    try:
        pages = extract_pdf(pdf_path)

    except (FileNotFoundError, ValueError) as error:
        print(f"PDF extraction error: {error}")
        return

    # Combine page text for the naive Q&A pipeline.
    pdf_text = "\n\n".join(
        page["text"] for page in pages
    )

    print(f"\nPDF loaded successfully: {len(pages)} page(s)")
    print("Ask questions about your document.")
    print("Press Ctrl+C or Ctrl+D to exit.\n")

    while True:
        try:
            question = input("You: ")

            if not question.strip():
                continue

            answer = ask_question(question, pdf_text)
            print(f"\nGemini: {answer}\n")

        except (EOFError, KeyboardInterrupt):
            print("\nConversation ended.")
            break

        except RuntimeError as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()
