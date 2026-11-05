import extract
import requests


user_prompt = input("Enter your question about the PDF: ").strip()

if not user_prompt:
    raise ValueError("A question is required.")

prompt = f"""Use the PDF text below to answer the user's question.
If the answer is not in the PDF, say so clearly and if asked to analyze or do something with the pdf then do so.

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