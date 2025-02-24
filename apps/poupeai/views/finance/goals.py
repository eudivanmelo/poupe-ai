from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from datetime import datetime
from apps.poupeai.mixins import PoupeAIMixin
from apps.poupeai.models import Goal, GoalDeposit
from apps.poupeai.views.generic.json import CreateJsonView, DeleteJsonView, UpdateJsonView
from django.shortcuts import get_object_or_404
from django.utils import timezone

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
    
class GoalDepositCreateView(CreateJsonView):
    '''
    View to create a deposit in a goal.
    '''
    success_url = reverse_lazy('goals')
    model = GoalDeposit
    fields = ['deposit_amount', 'deposit_at', 'note']
    success_message = "Depósito realizado com sucesso!"
    error_message = "Erro ao realizar depósito. Verifique os campos e tente novamente."
    
    def form_valid(self, form):
        # Obtém a meta associada ao depósito
        goal = get_object_or_404(Goal, pk=self.kwargs.get('pk'))
        form.instance.goal = goal
        
        # Validações
        if form.instance.deposit_at > timezone.now().date():
            return self.form_invalid(form)
        
        if form.instance.deposit_amount <= 0:
            return self.form_invalid(form)
        
        if form.instance.deposit_amount > goal.amount_needed:
            return self.form_invalid(form)
        
        if goal.completed_at:
            return self.form_invalid(form)
        
        super().form_valid(form)
        
        goal.save()
        
        if goal.amount_needed <= 0:
            goal.completed_at = timezone.now()
            goal.save()

        self.object = goal    
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'id': self.object.id, 'message': self.success_message})
        return HttpResponseBadRequest('Requisição inválida')
    
