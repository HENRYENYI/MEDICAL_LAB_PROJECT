# tests/admin.py

from django.contrib import admin
from .models import TestCategory, LabTest, TestPackage

# Keep this for the simple category and package admin
admin.site.register(TestCategory)
admin.site.register(TestPackage)

# Create a custom admin class for LabTest
@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    # How the list of tests will look
    list_display = ('name', 'category', 'price', 'is_available', 'is_best_seller')
    list_filter = ('category', 'is_available', 'is_best_seller')
    search_fields = ('name', 'short_description')
    list_editable = ('price', 'is_available', 'is_best_seller')

    # Organize the fields on the "Add/Edit Test" page into logical groups
    fieldsets = (
        ('Core Information', {
            'fields': ('name', 'category', 'price')
        }),
        ('Display Content', {
            'fields': ('short_description', 'long_description')
        }),
        ('Test Specifics', {
            'fields': ('sample_type', 'preparation', 'test_type', 'turnaround_time')
        }),
        ('Status & Visibility', {
            'fields': ('is_available', 'is_best_seller')
        }),
    )