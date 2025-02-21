from django.shortcuts import render

def dashboard_view(request):
    context = {"name" : "dashboard"}
    return render(request, 'dashboard.html', context)