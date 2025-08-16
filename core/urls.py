# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # The empty string '' means the root URL
    path('about/', views.about_view, name='about'),
]