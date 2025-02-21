from django.shortcuts import redirect, render
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import default_storage
from apps.poupeai.mixins import PoupeAIMixin
from django.contrib import messages

User = get_user_model()

class ProfileView(PoupeAIMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "poupeai/profile_page.html"
    fields = ['email', 'name', 'birth_date', 'sex', 'profile_picture']
    success_url = reverse_lazy('profile')
    success_message = "Perfil atualizado com sucesso!"

    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Perfil", "url": None},
        ]

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

class ProfileDeleteView(PoupeAIMixin, DeleteView):
    model = User
    template_name = "poupeai/profile_delete.html"
    success_url = reverse_lazy('home')

    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Perfil", "url": reverse_lazy('profile')},
            {"name": "Excluir Perfil", "url": None},
        ]

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        user = self.get_object()

        if user.check_password(password):
            user.delete()
            messages.success(request, 'Sua conta foi excluída com sucesso.')
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {
                'password_error': 'Senha incorreta. Tente novamente.',
            })