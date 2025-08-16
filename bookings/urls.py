# bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Cart and Checkout
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<str:item_type>/<int:item_id>/', views.cart_add, name='cart_add'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<str:booking_code>/', views.booking_success, name='booking_success'),

    # Result Checking
    path('check-result/', views.check_result_view, name='check_result'),
    path('result/<str:booking_code>/', views.result_detail_view, name='result_detail'),
]