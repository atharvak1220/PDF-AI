import os

from dotenv import load_dotenv
from pypdf import PdfReader

PDF_PATH = "/home/atharvak/Programming/Learning/AI/PDF project/PDF-AI/data/Tax.pdf"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.5-flash-lite:generateContent"
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Add it to your local .env file.")

reader = PdfReader(PDF_PATH)

pdf_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        pdf_text += text + "\n\n"

if not pdf_text:
    raise ValueError("No extractable text was found in the PDF.")

print(f"Loaded {len(reader.pages)} page(s) from the PDF.")

