from django.urls import path
from . import views

app_name = 'ai_doctor'

urlpatterns = [
    path('', views.ai_doctor_home, name='home'),
    path('ask/', views.ask_ai_doctor, name='ask'),
]