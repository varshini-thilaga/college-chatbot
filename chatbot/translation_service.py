from googletrans import Translator

translator = Translator()

def indic_to_english(text, chrome_lang):
    try:
        return translator.translate(text, dest="en").text
    except Exception:
        return text

def english_to_indic(text, chrome_lang):
    try:
        target = chrome_lang.split("-")[0]
        return translator.translate(text, dest=target).text
    except Exception:
        return text
