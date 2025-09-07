from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ConsultationSpecialty, ConsultationBooking
from .forms import ConsultationBookingForm

def consultation_home(request):
    specialties = ConsultationSpecialty.objects.filter(is_available=True).order_by('name')
    context = {
        'specialties': specialties,
    }
    return render(request, 'consultation/consultation_home.html', context)

def consultation_booking(request, specialty_id):
    specialty = get_object_or_404(ConsultationSpecialty, id=specialty_id, is_available=True)
    
    if request.method == 'POST':
        form = ConsultationBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.specialty = specialty
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            messages.success(request, 'Consultation booking submitted successfully!')
            return redirect('consultation:consultation_home')
    else:
        form = ConsultationBookingForm()
    
    context = {
        'specialty': specialty,
        'form': form,
    }
    return render(request, 'consultation/booking_form.html', context)