# tests/urls.py
from django.urls import path
from . import views

app_name = 'tests'  # This is good practice for namespacing

urlpatterns = [
    path('', views.test_list_view, name='test_list'),
    path('<int:pk>/', views.test_detail_view, name='test_detail'), # <-- ADD THIS LINE
     path('anonymous/', views.anonymous_test_list_view, name='anonymous_test_list'), # 
     path('anonymous/', views.anonymous_test_list_view, name='anonymous_test_list'),
]