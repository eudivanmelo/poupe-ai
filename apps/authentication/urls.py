from django.urls import path, include
from .views import SignInView, SignUpView, forgot_view, updatepassword_view, CustomLogoutView

urlpatterns = [
    path('signin/', SignInView.as_view(), name='sign-in'),
    path('signup/', SignUpView.as_view(), name='sign-up'),
    path('forgot/', forgot_view, name='forgot-password'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('update-password/', updatepassword_view, name='update-password'),
    path('social/', include('social_django.urls', namespace='social')),
]