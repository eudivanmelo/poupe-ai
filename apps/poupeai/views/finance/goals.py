from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from datetime import datetime
from apps.poupeai.mixins import PoupeAIMixin
from apps.poupeai.models import Goal
from apps.poupeai.views.generic.json import CreateJsonView, DeleteJsonView, UpdateJsonView

class GoalsListView(PoupeAIMixin, ListView):
    '''
    View to list all goals.
    '''
    template_name = "poupeai/goals_page.html"
    model = Goal
    context_object_name = "goals"

    def get_name(self):
        return "goals"
    
    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Minhas Metas", "url": None},
        ]

class GoalCreateView(CreateJsonView):
    '''
    View to create a new goal.
    '''
    success_url = reverse_lazy('goals')
    model = Goal
    fields = ['name', 'motivation', 'color', 'initial_balance', 'goal', 'target_at']
    success_message = "Meta criada com sucesso!"
    error_message = "Erro ao criar meta. Verifique os campos e tente novamente."
    
class GoalDeleteView(DeleteJsonView):
    '''
    View to delete a goal.
    '''
    success_url = reverse_lazy('goals')
    model = Goal
    success_message = "Meta deletada com sucesso!"
    error_message = "Erro ao deletar meta. Tente novamente."
    
class GoalUpdateView(UpdateJsonView):
    '''
    View to update a goal.
    '''
    model = Goal
    fields = ['name', 'motivation', 'color', 'initial_balance', 'goal', 'target_at']
    success_url = reverse_lazy('goals')
    context_object_name = 'goal'
    success_message = 'Meta atualizada com sucesso!'
    error_message = 'Ocorreu um erro ao atualizar a meta, verifique as informações ou tente novamente mais tarde.'
