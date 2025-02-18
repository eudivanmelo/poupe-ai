from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from apps.poupeai.mixins import PoupeAIMixin

class ProfileView(PoupeAIMixin, TemplateView):
    template_name = "poupeai/profile_page.html"
    
    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Perfil", "url": None},
        ]

class ProfileDeletionView(PoupeAIMixin, TemplateView):
    template_name = "poupeai/account_deletion.html"

    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Perfil", "url": reverse_lazy('profile')},
            {"name": "Solicitar Exclusão de Conta", "url": None},
        ]