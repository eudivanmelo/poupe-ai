from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import default_storage
from apps.poupeai.mixins import PoupeAIMixin

User = get_user_model()

class ProfileView(PoupeAIMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "poupeai/profile_page.html"
    fields = ['email', 'name', 'birth_date', 'sex', 'profile_picture']
    success_url = reverse_lazy('profile')
    success_message = "Perfil atualizado com sucesso!"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].disabled = True
        return form

class UpdateProfilePictureView(View):
    """ View para atualizar ou remover a foto do perfil via AJAX """
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
            user.save()
            return JsonResponse({'status': 'success', 'image_url': user.profile_picture.url})
        return JsonResponse({'status': 'error'}, status=400)

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.profile_picture:
            default_storage.delete(user.profile_picture.path)
        user.profile_picture = None
        user.save()
        return JsonResponse({'status': 'success', 'image_url': '/static/imgs/profile.png'})

class ProfileDeletionView(PoupeAIMixin, TemplateView):
    template_name = "poupeai/account_deletion.html"

    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Perfil", "url": reverse_lazy('profile')},
            {"name": "Solicitar Exclusão de Conta", "url": None},
        ]