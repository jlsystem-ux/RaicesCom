# Temporarily disabled for local development - uncomment for production
# from google.cloud import translate_v2 as translate

class TranslationService:
    def __init__(self):
        # self.client = translate.Client()
        pass

    def translate_text(self, text, target_lang, source_lang='auto'):
        if not text:
            return ''
        # For local development, return original text
        # In production, uncomment the lines below:
        # result = self.client.translate(text, target_language=target_lang, source_language=source_lang)
        # return result.get('translatedText', '')
        return f"[Translation disabled for local dev] {text}"
