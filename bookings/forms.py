
    # bookings/forms.py
from django import forms
from .models import HealthProfile, DoctorAccessCode
from datetime import datetime, timedelta

class AnonymousBookingForm(forms.Form):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    age = forms.IntegerField(
        min_value=1, 
        label="Your Age",
        widget=forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-main focus:ring-primary-main'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        label="Gender",
        widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-main focus:ring-primary-main'})
    )

class HealthProfileForm(forms.ModelForm):
    class Meta:
        model = HealthProfile
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'gender': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'blood_type': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'height': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'weight': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'allergies': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'medications': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300'}),
        }

class DoctorAccessForm(forms.Form):
    doctor_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300', 'placeholder': 'Doctor name (optional)'})
    )
    expires_in_days = forms.ChoiceField(
        choices=[(7, '7 days'), (30, '30 days'), (90, '90 days')],
        initial=30,
        widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300'})
    )