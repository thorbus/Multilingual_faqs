# apps/faqs/models.py
from django.db import models
from django.core.cache import cache
from django.conf import settings
from ckeditor.fields import RichTextField
from googletrans import Translator

class FAQ(models.Model):
    question = models.TextField(help_text="Question text in English")
    answer = RichTextField(help_text="Answer with rich text formatting")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Language-specific fields
    question_hi = models.TextField(blank=True, null=True, help_text="Hindi translation")
    question_bn = models.TextField(blank=True, null=True, help_text="Bengali translation")
    answer_hi = RichTextField(blank=True, null=True, help_text="Hindi answer")
    answer_bn = RichTextField(blank=True, null=True, help_text="Bengali answer")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]

    def get_translation(self, field_name, lang_code):
        """Get translated text for a given field and language."""
        cache_key = f'faq_{self.id}_{field_name}_{lang_code}'
        cached_value = cache.get(cache_key)
        
        if cached_value:
            return cached_value

        translated_field = f'{field_name}_{lang_code}'
        if hasattr(self, translated_field) and getattr(self, translated_field):
            translated_text = getattr(self, translated_field)
        else:
            # Only translate if there's text to translate
            original_text = getattr(self, field_name)
            if original_text:
                try:
                    translator = Translator()
                    translation = translator.translate(
                        original_text,
                        dest=lang_code,
                        src='en'
                    )
                    translated_text = translation.text if translation else original_text
                except Exception:
                    translated_text = original_text
            else:
                translated_text = ""

        # Cache the result
        cache.set(cache_key, translated_text, timeout=3600)  # Cache for 1 hour
        return translated_text

    def get_question(self, lang_code='en'):
        if lang_code == 'en':
            return self.question
        return self.get_translation('question', lang_code)

    def get_answer(self, lang_code='en'):
        if lang_code == 'en':
            return self.answer
        return self.get_translation('answer', lang_code)