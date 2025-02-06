from django.shortcuts import render
from django.views.generic import FormView
from apps.authentication.forms import SignUpForm
from django.contrib import messages
from django.urls import reverse_lazy

class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy("sign-in")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Sua conta foi criada com sucesso! Verifique seu e-mail para ativar sua conta.")
        return super().form_valid(form)
    