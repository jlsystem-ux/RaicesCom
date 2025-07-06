# services.py
from googletrans import Translator

class TranslationService:
    def __init__(self):
        self.translator = Translator()
    
    def translate_text(self, text, target_language, source_language='auto'):
        try:
            result = self.translator.translate(
                text, 
                src=source_language, 
                dest=target_language
            )
            return result.text
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def detect_language(self, text):
        try:
            result = self.translator.detect(text)
            return result.lang
        except Exception:
            return 'unknown'