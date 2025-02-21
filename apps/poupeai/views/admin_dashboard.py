from django.shortcuts import render

def admin_view(request):
    context = {"name" : "admin-dashboard"}
    return render(request, 'admin-dashboard.html', context)