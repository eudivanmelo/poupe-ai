from django.shortcuts import render

def updatepassword_view(request):
    return render(request, 'authentication/update-password.html')