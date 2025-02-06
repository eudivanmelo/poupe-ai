from django.shortcuts import render
from django.contrib import messages

def signin_view(request):
    messages.error(request, 'Invalid username or password')
    return render(request, 'signin.html')