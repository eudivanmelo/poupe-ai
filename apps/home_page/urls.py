from django.urls import path
from apps.home_page.views import home

urlpatterns = [
    path('views/', home),
]