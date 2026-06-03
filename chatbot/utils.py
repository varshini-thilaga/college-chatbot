import string
from langdetect import detect, LangDetectException
import re

INDIC_HINTS = {
    "ta": ["vanakam", "வணக்கம்"],
    "hi": ["namaste", "नमस्ते"],
    "ml": ["namaskaram", "നമസ്കാരം"],
    "kn": ["namaskara", "ನಮಸ್ಕಾರ"],
    "te": ["namaskaram", "నమస్కారం"],
}

def detect_language(text: str) -> str:
    t = text.lower().strip()

    # 1️⃣ Script-based detection (most reliable)
    if re.search(r"[அ-ஹ]", t):
        return "ta"
    if re.search(r"[अ-ह]", t):
        return "hi"
    if re.search(r"[അ-ഹ]", t):
        return "ml"
    if re.search(r"[ಅ-ಹ]", t):
        return "kn"
    if re.search(r"[అ-హ]", t):
        return "te"

    # 2️⃣ Known Indic greetings (romanized)
    for lang, words in INDIC_HINTS.items():
        if any(w in t for w in words):
            return lang

    # 3️⃣ Very short input → default English
    if len(t.split()) < 4:
        return "en"

    # 4️⃣ Fallback to langdetect
    try:
        return detect(t)
    except LangDetectException:
        return "en"



def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_query(text: str) -> str:
    t = text.lower().strip()
    t = t.strip(string.punctuation)
    return t


def format_bot_response(text: str) -> str:
    """
    Ensures all bot responses are structured and readable.
    - Normalizes bullet points
    - Preserves headings
    - Keeps spacing clean
    """
    if not text:
        return ""

    lines = text.strip().splitlines()
    formatted = []

    for line in lines:
        line = line.strip()

        if not line:
            formatted.append("")
            continue

        # Normalize bullets
        if line.startswith(("•", "-", "*")):
            formatted.append(f"- {line.lstrip('•-* ').strip()}")
        else:
            formatted.append(line)

    return "\n".join(formatted)


def small_talk(text: str):
    t = normalize_query(text)

    greetings = {
        "hi": "**Hello!**\n\nHow can I assist you today?",
        "hii": "**Hello!**\n\nHow can I assist you today?",
        "hiii": "**Hello!**\n\nHow can I help you?",
        "hello": "**Hello!**\n\nHow can I assist you today?",
        "hey": "**Hey!**\n\nWhat would you like to know?",
    }

    farewells = {
        "bye": "**Goodbye!**\n\nHave a great day!",
        "ok bye": "**Bye!**\n\nFeel free to ask anytime.",
        "good night": "**Good night!**\n\nSweet dreams 🌙",
        "goodbye": "**Goodbye!**\n\nWishing you all the best.",
    }

    for g in greetings:
        if t == g or t.startswith(g + " "):
            return greetings[g]

    for f in farewells:
        if t == f or t.startswith(f + " "):
            return farewells[f]

    if any(x in t for x in ["thank you", "thanks", "thanku", "thx"]):
        return "**You’re welcome!**\n\nIf you have more questions, feel free to ask."

    return None
