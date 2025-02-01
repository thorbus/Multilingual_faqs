from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from .models import FAQ
from .serializers import FAQSerializer

class FAQViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing FAQs with language support.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        """Optimize queryset with select_related if needed."""
        return FAQ.objects.all().order_by('-created_at')

    @method_decorator(cache_page(settings.CACHE_TIMEOUT))
    def list(self, request, *args, **kwargs):
        """List FAQs with caching support."""
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def languages(self, request):
        """Return list of supported languages."""
        return Response({
            'supported_languages': ['en', 'hi', 'bn'],
            'default_language': 'en'
        })