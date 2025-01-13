from django.contrib import admin

from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home_page.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('', include('apps.poupeai.urls')),
]
