
from pathlib import Path

from pypdf import PdfReader


def extract_pdf(pdf_path):
    pdf_path = Path(pdf_path)

    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text or not text.strip():
            continue

        pages.append({
            "text": text.strip(),
            "source_file": pdf_path.name,
            "page_number": page_number,
        })

    if not pages:
        raise ValueError("No extractable text was found in the PDF.")

    return pages


if __name__ == "__main__":
    pdf_path = Path(__file__).resolve().parents[1] / "data" / "Tax.pdf"

    pages = extract_pdf(pdf_path)

    print(f"Extracted text from {len(pages)} page(s).")

    for page in pages:
        print(
            f"Page {page['page_number']}: "
            f"{len(page['text'])} characters"
        )
