from deep_translator import GoogleTranslator


def indic_to_english(text: str, chrome_lang: str) -> str:
    try:
        lang = chrome_lang.split("-")[0]
        return GoogleTranslator(source=lang, target="en").translate(text)
    except Exception:
        return text


def english_to_indic(text: str, chrome_lang: str) -> str:
    try:
        lang = chrome_lang.split("-")[0]
        return GoogleTranslator(source="en", target=lang).translate(text)
    except Exception:
        return text
