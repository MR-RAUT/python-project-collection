from groq import Groq

# ==========================================================
# CONFIG (OLD METHOD – HARD CODED)
# ==========================================================

MODEL_NAME = "llama-3.1-8b-instant"

# ✅ PUT YOUR REAL KEY HERE
API_KEY = "your_groq_api_key_here"

client = Groq(api_key=API_KEY)


# ==========================================================
# AI CALL (TEXT ONLY – GROQ DOES NOT SUPPORT IMAGES)
# ==========================================================

def ask_ai(prompt: str) -> str:
    """
    Generate AI response.
    Used by:
    - Chat
    - Screen Analyzer (OCR text)
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are NovaDhi AI, an expert assistant.\n"
                "- Solve coding questions step by step\n"
                "- Answer MCQs with correct option\n"
                "- Explain theory briefly and clearly"
            )
        },
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.3,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"AI Error: {e}"
