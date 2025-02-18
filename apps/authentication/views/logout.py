from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from social_django.utils import load_strategy, load_backend

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('sign-in')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Logout realizado com sucesso! Esperamos ver você de volta em breve.")
        return super().dispatch(request, *args, **kwargs)