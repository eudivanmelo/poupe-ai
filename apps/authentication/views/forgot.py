from django.shortcuts import render

def forgot_view(request):
    return render(request, 'authentication/forgot-password.html')