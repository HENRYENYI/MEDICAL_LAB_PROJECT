from django.contrib import admin
from .models import ConsultationSpecialty, ConsultationBooking

@admin.register(ConsultationSpecialty)
class ConsultationSpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_minutes', 'is_available')
    list_editable = ('price', 'duration_minutes', 'is_available')
    search_fields = ('name', 'description')

@admin.register(ConsultationBooking)
class ConsultationBookingAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'specialty', 'preferred_date', 'preferred_time', 'status')
    list_filter = ('specialty', 'status', 'preferred_date')
    search_fields = ('name', 'email', 'user__username')
    list_editable = ('status',)
    
    def get_patient_name(self, obj):
        return obj.user.username if obj.user else obj.name
    get_patient_name.short_description = 'Patient'
