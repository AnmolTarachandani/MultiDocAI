# utils/translate.py

from deep_translator import GoogleTranslator

def translate_text(text, target_lang='en'):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        return f"Translation failed: {e}"
