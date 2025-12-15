def generate_hint(session, hint_level):
    context = build_chat_context(session)

    prompt = f"""
You are a coding assistant.

Conversation so far:
{context}

Generate a LEVEL {hint_level} hint.

Rules:
- No full solutions
- Match difficulty of level
- Be concise
"""

    return ask_gemini(prompt)
