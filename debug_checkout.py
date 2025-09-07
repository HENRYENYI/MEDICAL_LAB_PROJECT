#!/usr/bin/env python
"""
Debug script to test checkout functionality
Run this with: python debug_checkout.py
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_lab.settings')
django.setup()

from bookings.forms import AnonymousBookingForm
from bookings.models import Booking
from tests.models import LabTest, TestPackage

def test_form():
    """Test if the form validates correctly"""
    print("Testing AnonymousBookingForm...")
    
    # Test valid data
    form_data = {
        'age': 25,
        'gender': 'Male'
    }
    
    form = AnonymousBookingForm(data=form_data)
    if form.is_valid():
        print("✓ Form validation passed")
        print(f"  Cleaned data: {form.cleaned_data}")
    else:
        print("✗ Form validation failed")
        print(f"  Errors: {form.errors}")
    
    # Test invalid data
    invalid_form_data = {
        'age': -5,  # Invalid age
        'gender': 'Invalid'  # Invalid gender
    }
    
    invalid_form = AnonymousBookingForm(data=invalid_form_data)
    if not invalid_form.is_valid():
        print("✓ Form correctly rejects invalid data")
        print(f"  Errors: {invalid_form.errors}")
    else:
        print("✗ Form should have rejected invalid data")

def test_booking_creation():
    """Test if booking can be created"""
    print("\nTesting Booking creation...")
    
    try:
        booking = Booking.objects.create(
            age=30,
            gender='Female',
            total_price=100.00,
            status='PAID'
        )
        print(f"✓ Booking created successfully: {booking.booking_code}")
        
        # Clean up
        booking.delete()
        print("✓ Test booking cleaned up")
        
    except Exception as e:
        print(f"✗ Booking creation failed: {str(e)}")

def test_models():
    """Test if models are accessible"""
    print("\nTesting model access...")
    
    try:
        test_count = LabTest.objects.count()
        package_count = TestPackage.objects.count()
        booking_count = Booking.objects.count()
        
        print(f"✓ LabTest count: {test_count}")
        print(f"✓ TestPackage count: {package_count}")
        print(f"✓ Booking count: {booking_count}")
        
    except Exception as e:
        print(f"✗ Model access failed: {str(e)}")

if __name__ == "__main__":
    print("=== Checkout Debug Script ===")
    test_form()
    test_booking_creation()
    test_models()
    print("\n=== Debug Complete ===")