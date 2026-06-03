import os
import uuid
import hashlib
from gtts import gTTS
from django.conf import settings


LANG_MAP = {
    "en": "en",
    "en-US": "en",
    "ta": "ta",
    "ta-IN": "ta",
    "hi": "hi",
    "hi-IN": "hi",
    "te": "te",
    "te-IN": "te",
    "kn": "kn",
    "kn-IN": "kn",
    "ml": "ml",
    "ml-IN": "ml",
}


def generate_audio_url(text: str, chrome_lang: str) -> str:
    if not text.strip():
        return ""

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    # Normalize language
    gtts_lang = LANG_MAP.get(chrome_lang, "en")

    # Cache by hash of text + language
    text_hash = hashlib.md5(f"{text}_{gtts_lang}".encode()).hexdigest()
    filename = f"{text_hash}.mp3"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    # Return cached audio if exists
    if os.path.exists(filepath):
        return settings.MEDIA_URL + filename

    try:
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        tts.save(filepath)
    except Exception as e:
        print("TTS error:", e)
        return ""

    return settings.MEDIA_URL + filename
