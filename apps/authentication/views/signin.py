from django.shortcuts import render

def signin_view(request):
    return render(request, 'signin.html')