
import os

import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.5-flash-lite:generateContent"
)

API_KEY = os.getenv("GEMINI_API_KEY")


def ask_question(user_prompt, pdf_text):
    if not user_prompt.strip():
        raise ValueError("A question is required.")

    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set. Add it to your .env file."
        )

    prompt = f"""Use the PDF text below to answer the user's question.
If the answer is not in the PDF, say so clearly.

User's question:
{user_prompt}

PDF text:
---
{pdf_text}
---
"""

    try:
        response = requests.post(
            GEMINI_URL,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": API_KEY,
            },
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            },
            timeout=(10, 60),
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            f"Gemini request failed: {error}"
        ) from error

    result = response.json()

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]

    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError(
            f"Unexpected Gemini response: {result}"
        ) from error
