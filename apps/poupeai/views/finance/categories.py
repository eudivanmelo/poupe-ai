from django.urls import reverse_lazy
from django.views.generic import ListView

from apps.poupeai.mixins import PoupeAIMixin
from apps.poupeai.models import Category
from apps.poupeai.views.generic.json import CreateJsonView, DeleteJsonView, UpdateJsonView

class CategoriesListView(PoupeAIMixin, ListView):
    '''
    View for listing all categories
    '''

    template_name = 'poupeai/categories_page.html'
    model = Category
    context_object_name = 'categories'

    def get_name(self):
        return "categories"
    
    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Categories", "url": None},
        ]
    
    def get_queryset(self):
        '''Filters categories by the logged-in user'''
        return super().get_queryset().filter(user=self.request.user)
    
    def _get_categories_by_type(self, category_type):
        '''Returns categories filtered by type (expense/income)'''
        return self.get_queryset().filter(type=category_type)
    
    def _calculate_total_value(self, categories):
        '''Calculates the total value of the provided categories'''
        return sum(category.total_transactions_value for category in categories)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        expense_categories = self._get_categories_by_type('expense')
        income_categories = self._get_categories_by_type('income')

        total_expense_categories = expense_categories.count()
        total_income_categories = income_categories.count()
        total_expenses = self._calculate_total_value(expense_categories)
        total_income = self._calculate_total_value(income_categories)

        context.update({
            "expense_categories": expense_categories,
            "income_categories": income_categories,
            "total_expense_categories": total_expense_categories,
            "total_income_categories": total_income_categories,
            "total_expenses": total_expenses,
            "total_income": total_income,
        })

        return context

class CategoryCreateView(CreateJsonView):
    '''
    View for creating a new category
    '''
    success_url = reverse_lazy('categories')
    model = Category
    fields = ['name', 'color', 'type']
    success_message = 'Categoria criada com sucesso!'
    error_message = 'Ocorreu um erro ao criar a categoria, verifique as informações ou tente novamente mais tarde.'

class CategoryDeleteView(DeleteJsonView):
    '''
    View for deleting an category
    '''
    success_url = reverse_lazy('categories')
    model = Category
    success_message = 'Categoria deletada com sucesso!'
    error_message = 'Ocorreu um erro ao deletar a categoria, verifique as informações ou tente novamente mais tarde.'

class CategoryUpdateView(UpdateJsonView):
    '''
    View for updating an category
    '''
    model = Category
    fields = ['name', 'color']
    success_url = reverse_lazy('categories')
    context_object_name = 'category'
    success_message = 'Categoria atualizada com sucesso!'
    error_message = 'Ocorreu um erro ao atualizar a categoria, verifique as informações ou tente novamente mais tarde.'