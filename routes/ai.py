# routes/ai.py
from flask import Blueprint, request, jsonify
from services.openai_client import client, MODEL
import difflib

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

# ------------------------
# Constants
# ------------------------
SOLUTION_SEEKING_PATTERNS = [
    "give me the solution",
    "full code",
    "complete code",
    "final answer",
    "solve this",
    "write the function",
    "just tell me",
]

SOLUTION_SIGNALS = ["def ", "return ", "class ", "for ", "while "]

# ------------------------
# Helpers
# ------------------------
def is_solution_seeking(message: str) -> bool:
    return any(p in message.lower() for p in SOLUTION_SEEKING_PATTERNS)

def normalize(code: str) -> str:
    return "\n".join(line.strip() for line in code.splitlines() if line.strip())

def code_changed(old: str, new: str) -> bool:
    diff = list(difflib.unified_diff(old.splitlines(), new.splitlines()))
    return len(diff) > 4

def analyze_code(code: str):
    return {
        "has_code": bool(code.strip()),
        "lines": len(code.strip().splitlines()),
        "has_loop": any(k in code for k in ["for ", "while "]),
        "has_condition": "if " in code,
    }

def is_user_stuck(code: str, attempts: int) -> bool:
    stats = analyze_code(code)
    if not stats["has_code"]:
        return False
    if attempts >= 3 and stats["lines"] < 5:
        return True
    if attempts >= 2 and stats["has_loop"] and not stats["has_condition"]:
        return True
    return False

# ------------------------
# Route
# ------------------------
@ai_bp.route("/chat", methods=["POST"])
def ai_chat():
    data = request.json or {}

    # ------------------------
    # Extract inputs
    # ------------------------
    problem = data.get("problem") or data.get("context", {}).get("problem", {})
    user_message = data.get("message", "")
    user_code = data.get("code") or data.get("context", {}).get("code", "")
    previous_code = data.get("previousCode", "")
    history = data.get("history", [])

    mode = data.get("mode", "CHAT")  # CHAT | HINT | DEBUG
    hint_level = int(data.get("hintLevel", 1))
    attempts = int(data.get("attempts", 0))

    title = problem.get("title", "No Title")
    difficulty = problem.get("difficulty", "Unknown")
    description = problem.get("description", "")
    constraints = ", ".join(
        c.get("content", "") for c in problem.get("constraints", [])
    )

    # ------------------------
    # Anti-cheat
    # ------------------------
    if is_solution_seeking(user_message):
        return jsonify({
            "success": True,
            "data": {
                "text": "I can’t give the full solution directly. Let’s work through it step by step 👍"
            }
        })

    # ------------------------
    # Code-diff gating for hints
    # ------------------------
    if mode == "HINT" and not code_changed(
        normalize(previous_code), normalize(user_code)
    ):
        return jsonify({
            "success": True,
            "data": {
                "text": "Try making a small change in your code first — even a minor edit helps unlock the next hint."
            }
        })

    # ------------------------
    # Auto hint escalation
    # ------------------------
    if is_user_stuck(user_code, attempts) and hint_level < 3:
        hint_level += 1

    # ==========================================================
    # DEBUG MODE (AI-based error detection, NO fixing)
    # ==========================================================
    if mode == "DEBUG":
        system_prompt = (
            "You are an AI code reviewer inside a coding platform.\n"
            "Identify potential mistakes in the user's code.\n"
            "Do NOT fix the code.\n"
            "Do NOT provide a full solution.\n"
            "Explain where the issue is and why it may be wrong.\n"
            "Be concise and structured."
        )

        user_prompt = f"""
Analyze the following code and report possible issues.

Rules:
- Do NOT rewrite or fix the code
- Do NOT provide full solutions
- Point out the issue location
- Explain the reasoning
- Provide a conceptual hint only

Problem:
{description}

User Code:
{user_code if user_code else "No code provided."}
"""

        try:
            response = client.responses.create(
                model=MODEL,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_output_tokens=250,
                temperature=0.2,
            )

            text = response.output_text or ""

            # Safety net: prevent solution leakage
            if sum(s in text for s in SOLUTION_SIGNALS) >= 3:
                text = (
                    "I see a potential issue, but let’s reason about it step by step. "
                    "Focus on how your logic behaves at the boundaries."
                )

            return jsonify({
                "success": True,
                "data": {
                    "type": "debug",
                    "text": text
                }
            })

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    # ==========================================================
    # CHAT / HINT MODE
    # ==========================================================
    system_prompt = (
        "You are a friendly AI coding assistant inside a coding platform. "
        "Guide users step by step without giving full solutions."
    )

    user_prompt = f"""
**ANTI-CHEAT RULES**
- Never provide the full solution
- Never rewrite the entire code
- Partial snippets only at hint level L3

**MOTIVATION RULES**
- Acknowledge effort
- Encourage next step

MODE: {mode}
HINT_LEVEL: L{hint_level}

PROBLEM:
Title: {title}
Difficulty: {difficulty}

Description:
{description}

Constraints:
{constraints}

User Code:
{user_code if user_code else "No code written yet."}

User Message:
{user_message}
"""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        if msg.get("role") in ("user", "assistant"):
            messages.append(msg)
    messages.append({"role": "user", "content": user_prompt})

    try:
        response = client.responses.create(
            model=MODEL,
            input=messages,
            max_output_tokens=400,
            temperature=0.4,
        )

        text = response.output_text or ""

        # Final safety net
        if sum(s in text for s in SOLUTION_SIGNALS) >= 3:
            text = (
                "Let’s slow down and focus on one idea at a time. "
                "What should happen in the next step of your logic?"
            )

        return jsonify({"success": True, "data": {"text": text}})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
