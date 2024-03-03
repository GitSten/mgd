# reliefmigrainerecipes/urls.py

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('diary.urls')),
    # Adjust the login and logout URLs

    # Keep the signup URL if you have a custom signup view

]