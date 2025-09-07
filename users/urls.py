
# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('health-profile/', views.health_profile_view, name='health_profile'),
    path('generate-doctor-code/', views.generate_doctor_code, name='generate_doctor_code'),
    path('doctor-access/<str:code>/', views.doctor_access_view, name='doctor_access'),
]