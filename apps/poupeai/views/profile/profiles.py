from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
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

    def form_valid(self, form):
        user = self.object

        if self.request.POST.get('remove_profile_picture') == '1':
            if user.profile_picture:
                default_storage.delete(user.profile_picture.path)
                user.profile_picture = None

        if 'profile_picture' in self.request.FILES:
            user.profile_picture = self.request.FILES['profile_picture']

        return super().form_valid(form)

class ProfileDeletionView(PoupeAIMixin, TemplateView):
    template_name = "poupeai/account_deletion.html"

    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Perfil", "url": reverse_lazy('profile')},
            {"name": "Solicitar Exclusão de Conta", "url": None},
        ]