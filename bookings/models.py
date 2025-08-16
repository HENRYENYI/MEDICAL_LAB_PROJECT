from django.db import models

# Create your models here.
# bookings/models.py
import uuid
from django.db import models
from django.conf import settings
from tests.models import LabTest, TestPackage

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING_PAYMENT', 'Pending Payment'),
        ('PAID', 'Paid, Awaiting Sample'),
        ('SAMPLE_COLLECTED', 'Sample Collected'),
        ('COMPLETED', 'Completed, Result Ready'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Unique code for BOTH anonymous and registered users
    booking_code = models.CharField(max_length=10, unique=True, blank=True)
    
    # For registered users (can be blank for anonymous)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    # For anonymous users
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    
    # The test(s) being booked
    tests = models.ManyToManyField(LabTest, blank=True)
    package = models.ForeignKey(TestPackage, on_delete=models.SET_NULL, null=True, blank=True)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING_PAYMENT')
    
    # Field for admin to upload the result
    result_file = models.FileField(upload_to='test_results/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.booking_code:
            # Generate a simple, human-readable unique code
            self.booking_code = str(uuid.uuid4().hex[:8]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_code}"