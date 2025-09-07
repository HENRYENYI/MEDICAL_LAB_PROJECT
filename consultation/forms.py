from django import forms
from .models import ConsultationBooking

class ConsultationBookingForm(forms.ModelForm):
    class Meta:
        model = ConsultationBooking
        fields = ['name', 'email', 'phone', 'preferred_date', 'preferred_time', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300', 'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300', 'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300', 'placeholder': '+234 xxx xxx xxxx'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'preferred_time': forms.TimeInput(attrs={'type': 'time', 'class': 'mt-1 block w-full rounded-md border-gray-300'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'mt-1 block w-full rounded-md border-gray-300', 'placeholder': 'Any additional information or questions...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required for anonymous users
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True