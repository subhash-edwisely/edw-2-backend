import google.generativeai as genai
from flask import current_app
import logging

def ask_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the AI response text.
    """

    api_key = current_app.config.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    try:
        # Configure Gemini once per request
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.4,
                "top_p": 0.9,
                "max_output_tokens": 1024,
            },
            safety_settings={
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            },
        )

        response = model.generate_content(prompt)

        if not response or not response.text:
            return "⚠️ I couldn't generate a response. Try rephrasing your question."

        return response.text.strip()

    except Exception as e:
        logging.exception("Gemini API Error")
        return "⚠️ AI service is currently unavailable. Please try again later."
