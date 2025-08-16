# bookings/admin.py

from django.contrib import admin
from .models import Booking  # Import the Booking model from this app

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_code', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('booking_code', 'user__username')