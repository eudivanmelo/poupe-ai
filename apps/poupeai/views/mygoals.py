from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import datetime

def mygoals_view(request):
    goals = [
        {
            'id': 1,
            'name': 'Comprar uma Casa',
            'initial_balance': 5000.00,
            'goal_amount': 150000.00,
            'goal_date': datetime(2026, 12, 1).date(),
            'motivation': 'Minha Motivação Minha Motivação Minha Motivação',
            'goal_color': '#ff5733',
            'total_saved': 15000.00
        },
        {
            'id': 2,
            'name': 'Viajar para Europa',
            'initial_balance': 2000.00,
            'goal_amount': 30000.00,
            'goal_date': datetime(2025, 8, 1).date(),
            'motivation': 'Conhecer novos lugares e culturas',
            'goal_color': '#33ff57',
            'total_saved': 8000.00
        },
    ]

    current_date = datetime.now().date()

    for goal in goals:
        difference = goal['goal_amount'] - goal['total_saved']

        months_left = (goal['goal_date'].year - current_date.year) * 12 + goal['goal_date'].month - current_date.month
        if months_left < 0:
            months_left = 0

        if months_left > 0:
            monthly_amount_needed = (goal['goal_amount'] - goal['total_saved']) / months_left
        else:
            monthly_amount_needed = 0

        goal.update({
            'months_left': months_left,
            'monthly_amount_needed': monthly_amount_needed,
            'difference': difference
        })

    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Minhas Metas", "url": None},
    ]

    context = {
        "breadcrumbs": breadcrumbs, 
        "goals": goals, 
        "name" : "my-goals"
    }

    return render(request, 'my-goals.html', context)