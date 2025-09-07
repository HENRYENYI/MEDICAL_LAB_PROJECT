# tests/urls.py
from django.urls import path
from . import views

app_name = 'tests'  # This is good practice for namespacing

urlpatterns = [
    path('', views.test_list_view, name='test_list'),
    path('<int:pk>/', views.test_detail_view, name='test_detail'),
    path('anonymous/', views.anonymous_test_list_view, name='anonymous_test_list'),
    path('categories/', views.category_list_view, name='category_list'),
    path('category/<int:pk>/', views.category_detail_view, name='category_detail'),
]