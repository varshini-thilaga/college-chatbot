import os
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor

from langdetect import detect

from .simple_style import simple_answer
from .translation_service import indic_to_english, english_to_indic
from .tts_service import generate_audio_url


DATA_FILE = getattr(settings, "DATA_FILE", settings.BASE_DIR / 'chatbot' / 'college_data.txt')

try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        PDF_TEXT = f.read()
except Exception:
    PDF_TEXT = ""

_tts_executor = ThreadPoolExecutor(max_workers=2)


def cleanup_old_audio():
    media_path = settings.MEDIA_ROOT
    hours = getattr(settings, 'AUDIO_CLEANUP_HOURS', 24)
    cutoff = datetime.now() - timedelta(hours=hours)
    try:
        for file in os.listdir(media_path):
            if file.endswith('.mp3'):
                filepath = os.path.join(media_path, file)
                if os.path.getmtime(filepath) < cutoff.timestamp():
                    os.remove(filepath)
    except Exception:
        pass


def detect_lang_code(text: str) -> str:
    try:
        lang = detect(text)
    except Exception:
        lang = "en"
    return {
        "ta": "ta-IN",
        "kn": "kn-IN",
        "hi": "hi-IN",
        "te": "te-IN",
        "ml": "ml-IN",
        "en": "en"
    }.get(lang, "en")


def chat_view(request):

    if request.method == "GET" and not request.session.get("chat_initialized"):
        request.session["chat_history"] = []
        request.session["chat_initialized"] = True

    chat_history = request.session.get("chat_history", [])

    if request.method == "POST":

        if "clear_chat" in request.POST:
            cleanup_old_audio()
            request.session.flush()
            return redirect("chat")

        user_text = request.POST.get("message", "").strip()
        if not user_text:
            return redirect("chat")

        user_lang = detect_lang_code(user_text)
        now = timezone.now().strftime("%I:%M %p")

        chat_history.append({"sender": "user", "text": user_text, "time": now})

        # Translate to English if needed
        english_query = user_text if user_lang == "en" else indic_to_english(user_text, user_lang)

        # Get bot answer
        english_reply = simple_answer(english_query, PDF_TEXT, {})

        # Translate back if needed
        final_reply = english_reply if user_lang == "en" else english_to_indic(english_reply, user_lang)

        tts_lang = user_lang.split("-")[0]

        # Generate audio synchronously (cached responses return instantly)
        audio_url = generate_audio_url(final_reply, tts_lang)

        chat_history.append({
            "sender": "bot",
            "text": final_reply,
            "time": timezone.now().strftime("%I:%M %p"),
            "audio_url": audio_url
        })

        request.session["chat_history"] = chat_history
        return redirect("chat")

    return render(request, "chatbot/chat.html", {"chat_history": chat_history})