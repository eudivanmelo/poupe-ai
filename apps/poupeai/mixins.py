from django.contrib.auth.mixins import LoginRequiredMixin

class PoupeAIMixin(LoginRequiredMixin):
    breadcrumbs = []
    name = ""

    def get_breadcrumbs(self):
        return self.breadcrumbs
    
    def get_name(self):
        return self.name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.get_breadcrumbs()
        context["name"] = self.get_name()
        return context