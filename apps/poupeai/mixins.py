from django.urls import reverse_lazy

class BreadcrumbMixin:
    breadcrumbs = []

    def get_breadcrumbs(self):
        return self.breadcrumbs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.get_breadcrumbs()
        return context

class PageNameMixin:
    name = ""

    def get_name(self):
        return self.name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.get_name()
        return context