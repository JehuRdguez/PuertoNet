# myapp/context_processors.py
from .models import APIKey

def tinymce_api_key(request):
    try:
        api_key = APIKey.objects.get(service_name='TinyMCE')  # Asegúrate de que el nombre coincida
        return {'tinymce_api_key': api_key.key}
    except APIKey.DoesNotExist:
        return {'tinymce_api_key': None}
