from django.shortcuts import render

def updatepassword_view(request):
    return render(request, 'update-password.html')