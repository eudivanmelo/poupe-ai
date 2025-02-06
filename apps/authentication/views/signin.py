from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.authentication.forms import SignInForm
from django.contrib import messages

class SignInView(LoginView):
    template_name = 'signin.html'
    authentication_form = SignInForm
    next_page = reverse_lazy('dashboard')
    
    def form_invalid(self, form):
        messages.error(self.request, "Usuário ou senha inválidos!")
        return super().form_invalid(form)
    