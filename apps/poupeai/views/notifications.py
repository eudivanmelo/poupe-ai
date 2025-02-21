from django.shortcuts import render

def notifications_view(request):
    return render(request, 'notifications.html')