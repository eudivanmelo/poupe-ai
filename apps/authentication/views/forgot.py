from django.shortcuts import render

def forgot_view(request):
    return render(request, 'forgot-password.html')