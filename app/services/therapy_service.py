from __future__ import annotations

import random
import re
from pathlib import Path

SYSTEM_PROMPT_PATH = Path(__file__).resolve().parents[2] / "system.md"


def load_system_prompt() -> str:
    try:
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "You are a therapeutic support assistant."


SYSTEM_PROMPT = load_system_prompt()


IGD_PATTERNS = [r"game", r"gaming", r"video game", r"play.*game", r"gamer"]
BDD_PATTERNS = [r"body image", r"mirror", r"appearance", r"looks", r"body dysmorphic", r"BDD"]
DISTRESS_PATTERNS = [r"suicid", r"die", r"kill myself", r"hurt myself", r"want to disappear", r"can\'t go on"]


def detect_domain(message: str) -> str:
    normalized = message.lower()
    if any(re.search(pattern, normalized) for pattern in IGD_PATTERNS):
        return "IGD"
    if any(re.search(pattern, normalized) for pattern in BDD_PATTERNS):
        return "BDD"
    return "GENERAL"


def is_severe_distress(message: str) -> bool:
    normalized = message.lower()
    return any(re.search(pattern, normalized) for pattern in DISTRESS_PATTERNS)


def get_provider_label(api_key: str | None) -> str:
    if not api_key:
        return "local therapy support"
    key = api_key.strip()
    if key.upper().startswith("GEMINI"):
        return "Gemini"
    if key.upper().startswith("GROQ"):
        return "Groq"
    return "local therapy support"


def build_therapy_response(message: str, api_key: str | None = None) -> str:
    provider = get_provider_label(api_key)
    domain = detect_domain(message)
    distress = is_severe_distress(message)

    if distress:
        response = (
            "I'm hearing a lot of pain and urgency in what you're sharing."
            " If you are feeling overwhelmed or unsafe, it can really help to reach out to someone you trust or a professional right now."
            " You deserve immediate support."
        )
    else:
        if domain == "IGD":
            response = (
                "It sounds like gaming is taking up more of your energy than you want it to, and that can feel frustrating."
                " One small step could be setting a short, manageable break and noticing what urges come up during that time."
                " You might also try writing down what usually leads you back to the game so you can spot patterns without judging yourself."
            )
        elif domain == "BDD":
            response = (
                "I hear that your body image concerns are weighing on you, and that can feel really heavy."
                " When those thoughts come up, it may help to gently question them and remind yourself of qualities that are not about appearance."
                " A grounding exercise like naming three things you appreciate about your strengths or actions can also shift the focus a little."
            )
        else:
            response = (
                "I'm hearing how difficult this is for you, and it makes sense to feel overwhelmed."
                " One helpful approach can be to pause and notice the feeling without trying to push it away, then choose one small step you can take that feels manageable."
                " That could be a brief breathing break, a short walk, or simply giving yourself permission to rest."
            )

    if provider != "local therapy support":
        response += f"\n\nI'm responding using the {provider} support path, with your care and safety in mind."

    response += (
        "\n\nI'm not a substitute for a licensed mental health professional, but I'm here to support you."
    )
    return response
