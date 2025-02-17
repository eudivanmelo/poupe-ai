from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.authentication.forms import SignInForm
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.http import url_has_allowed_host_and_scheme

class SignInView(LoginView):
    template_name = 'authentication/signin.html'
    authentication_form = SignInForm
    next_page = reverse_lazy('dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=self.request.get_host()):
            return next_url
        return reverse_lazy('dashboard')  # Página padrão caso `next` não esteja definido
    
    def form_invalid(self, form):
        messages.error(self.request, "Usuário ou senha inválidos!")
        return super().form_invalid(form)
    