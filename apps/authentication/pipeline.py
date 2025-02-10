from django.core.exceptions import ValidationError
from apps.authentication.models import CustomUser

def save_profile(backend, user: CustomUser, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        user.name = response.get('given_name')
        user.save()
        
        