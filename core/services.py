from google.cloud import translate_v2 as translate

class TranslationService:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text, target_lang, source_lang='auto'):
        if not text:
            return ''
        result = self.client.translate(text, target_language=target_lang, source_language=source_lang)
        return result.get('translatedText', '')
