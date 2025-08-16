from django.urls import path
from . import views

app_name = 'consultation'

urlpatterns = [
    path('', views.consultation_home, name='consultation_home'),
]