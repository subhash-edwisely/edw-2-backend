from db import db
from models.chat_session import ChatSession
from models.chat_message import ChatMessage, MessageRole
from services.gemini_service import ask_gemini
from datetime import datetime

def get_or_create_session(user_id, problem_id):
    session = ChatSession.query.filter_by(
        user_id=user_id,
        problem_id=problem_id
    ).first()

    if not session:
        session = ChatSession(user_id=user_id, problem_id=problem_id)
        db.session.add(session)
        db.session.commit()

    return session


def add_message(session, role, content):
    msg = ChatMessage(
        session_id=session.id,
        role=role,
        content=content
    )
    session.last_message_at = datetime.utcnow()
    db.session.add(msg)
    db.session.commit()
    return msg


def handle_user_message(user_id, problem_id, message, code):
    session = get_or_create_session(user_id, problem_id)

    add_message(session, MessageRole.user, message)

    context = build_chat_context(session)

    prompt = f"""
You are a coding assistant.

Conversation so far:
{context}

User code:
{code}

Rules:
- Give hints and debugging help
- Do NOT give full solutions unless explicitly asked
- Be concise
"""

    ai_text = ask_gemini(prompt)

    add_message(session, MessageRole.ai, ai_text)
    return ai_text


def get_chat_history_for_problem(user_id, problem_id):
    session = ChatSession.query.filter_by(
        user_id=user_id,
        problem_id=problem_id
    ).first()

    if not session:
        return []

    return session.messages


MAX_CONTEXT_MESSAGES = 12

def build_chat_context(session):
    messages = session.messages[-MAX_CONTEXT_MESSAGES:]

    context = []
    for msg in messages:
        role = "User" if msg.role == MessageRole.user else "Assistant"
        context.append(f"{role}: {msg.content}")

    return "\n".join(context)

SUMMARY_TRIGGER = 30
SUMMARY_KEEP_LAST = 8

def maybe_summarize(session):
    if len(session.messages) < SUMMARY_TRIGGER:
        return

    old_messages = session.messages[:-SUMMARY_KEEP_LAST]

    summary_prompt = """
Summarize the following coding discussion briefly.
Focus on:
- Problem understanding
- Key hints
- Bugs discussed

Conversation:
""" + "\n".join(
        f"{m.role.value}: {m.content}" for m in old_messages
    )

    summary = ask_gemini(summary_prompt)

    # Delete old messages
    for m in old_messages:
        db.session.delete(m)

    # Add system summary
    db.session.add(ChatMessage(
        session_id=session.id,
        role=MessageRole.system,
        content=f"📌 Conversation Summary:\n{summary}"
    ))

    db.session.commit()
