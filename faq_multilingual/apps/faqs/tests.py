import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.faqs.models import FAQ
from django.core.cache import cache

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_faq():
    return FAQ.objects.create(
        question="What is Django?",
        answer="Django is a web framework for Python."
    )

@pytest.mark.django_db
class TestFAQModel:
    def test_faq_creation(self, sample_faq):
        """Test FAQ model creation"""
        assert FAQ.objects.count() == 1
        assert sample_faq.question == "What is Django?"

    def test_str_representation(self, sample_faq):
        """Test string representation of FAQ"""
        assert str(sample_faq) == "What is Django?"

    def test_translation_retrieval(self, sample_faq):
        """Test getting translations"""
        # Test Hindi translation
        hindi_question = sample_faq.get_question(lang_code='hi')
        assert hindi_question != ""
        assert hindi_question != sample_faq.question

        # Test Bengali translation
        bengali_question = sample_faq.get_question(lang_code='bn')
        assert bengali_question != ""
        assert bengali_question != sample_faq.question

    def test_caching(self, sample_faq):
        """Test if translations are being cached"""
        cache.clear()
        
        # First call should cache the translation
        hindi_question = sample_faq.get_question(lang_code='hi')
        cache_key = f'faq_{sample_faq.id}_question_hi'
        
        # Check if translation is cached
        cached_value = cache.get(cache_key)
        assert cached_value is not None
        assert cached_value == hindi_question

@pytest.mark.django_db
class TestFAQAPI:
    def test_create_faq(self, api_client):
        """Test creating a new FAQ"""
        url = reverse('faq-list')
        data = {
            'question': 'Test Question',
            'answer': 'Test Answer'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert FAQ.objects.count() == 1
        assert FAQ.objects.get().question == 'Test Question'

    def test_list_faqs(self, api_client, sample_faq):
        """Test listing FAQs"""
        url = reverse('faq-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_get_faq_in_hindi(self, api_client, sample_faq):
        """Test getting FAQ in Hindi"""
        url = f"{reverse('faq-list')}?lang=hi"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['question'] != sample_faq.question
        
    def test_update_faq(self, api_client, sample_faq):
        """Test updating an FAQ"""
        url = reverse('faq-detail', kwargs={'pk': sample_faq.pk})
        data = {
            'question': 'Updated Question',
            'answer': 'Updated Answer'
        }
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert FAQ.objects.get().question == 'Updated Question'

    def test_delete_faq(self, api_client, sample_faq):
        """Test deleting an FAQ"""
        url = reverse('faq-detail', kwargs={'pk': sample_faq.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert FAQ.objects.count() == 0