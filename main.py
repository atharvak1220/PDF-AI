import os

import requests
from dotenv import load_dotenv
from pypdf import PdfReader

PDF_PATH = "/home/atharvak/Downloads/Resume.pdf"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.5-flash-lite:generateContent"
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Add it to your local .env file.")

reader = PdfReader(PDF_PATH)
pdf_text = "\n\n".join(
    page.extract_text() or "" for page in reader.pages
).strip()

if not pdf_text:
    raise ValueError("No extractable text was found in the PDF.")

print(f"Loaded {len(reader.pages)} page(s) from the PDF.")

user_prompt = input("Enter your question about the PDF: ").strip()

if not user_prompt:
    raise ValueError("A question is required.")

prompt = f"""Use the PDF text below to answer the user's question.
If the answer is not in the PDF, say so clearly and if asked to analyze or do something with the pdf then do so.

User's question:
{user_prompt}

PDF text:
---
{pdf_text}
---
"""

try:
    print("Asking Gemini...", flush=True)
    response = requests.post(
        GEMINI_URL,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=(10, 60),
    )
    response.raise_for_status()
except requests.RequestException as error:
    raise SystemExit(f"Gemini request failed: {error}") from error

result = response.json()
try:
    answer = result["candidates"][0]["content"]["parts"][0]["text"]
except (KeyError, IndexError) as error:
    raise SystemExit(f"Gemini returned an unexpected response: {result}") from error

print(f"\nGemini response:\n{answer}")
