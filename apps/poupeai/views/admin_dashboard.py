from django.shortcuts import render

def admin_view(request):
    context = {"name" : "admin-dashboard"}
    return render(request, 'poupeai/admin_dashboard.html', context)