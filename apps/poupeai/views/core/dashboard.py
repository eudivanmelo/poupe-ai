from django.shortcuts import render

def dashboard_view(request):
    context = {"name" : "dashboard"}
    return render(request, 'poupeai/dashboard.html', context)