from django.urls import path
from .views import SignInView, SignUpView, forgot_view, updatepassword_view

urlpatterns = [
    path('signin/', SignInView.as_view(), name='sign-in'),
    path('signup/', SignUpView.as_view(), name='sign-up'),
    path('forgot/', forgot_view, name='forgot-password'),
    path('update-password/', updatepassword_view, name='update-password'),
]