
import requests
from . import extract


def ask_question(user_prompt):

    if not user_prompt.strip():
        raise ValueError("A question is required.")

    prompt = f"""Use the PDF text below to answer the user's question.
    If the answer is not in the PDF, say so clearly.

    User's question:
    {user_prompt}

    PDF text:
    ---
    {extract.pdf_text}
    ---
    """

    try:
        print("Asking Gemini...", flush=True)

        response = requests.post(
            extract.GEMINI_URL,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": extract.api_key,
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
        raise RuntimeError(f"Gemini request failed: {error}") from error

    result = response.json()

    try:
        answer = result["candidates"][0]["content"]["parts"][0]["text"]

    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError(f"Unexpected Gemini response: {result}") from error

    return answer
