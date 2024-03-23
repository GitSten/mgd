from django.urls import path
from . import views
from .views import SignUpView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'diary'  # This is for namespacing your URLs

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('add/', views.add_entry, name='add_entry'),
    path('types/', views.types, name='types'),
    path('recipes/', views.recipes, name='recipes'),
    path('signup/', views.SignUpView.as_view(), name='register'),
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),


    # Login and Logout URLs using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
