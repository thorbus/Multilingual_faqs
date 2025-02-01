# apps/faqs/serializers.py
from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']

    def to_representation(self, instance):
        lang = self.context.get('request').query_params.get('lang', 'en')
        data = super().to_representation(instance)
        
        if lang != 'en':
            data['question'] = instance.get_question(lang)
            data['answer'] = instance.get_answer(lang)
        
        return data