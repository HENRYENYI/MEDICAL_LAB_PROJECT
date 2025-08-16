
    # bookings/forms.py
from django import forms

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