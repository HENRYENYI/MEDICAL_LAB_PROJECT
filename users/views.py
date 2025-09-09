

# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from bookings.models import Booking, HealthProfile, DoctorAccessCode
from bookings.forms import HealthProfileForm, DoctorAccessForm
from datetime import datetime, timedelta



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please complete your health profile.')
            # Log the user in automatically
            from django.contrib.auth import login
            login(request, user)
            return redirect('users:health_profile_setup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def dashboard_view(request):
    # Get bookings for the currently logged-in user
    all_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    pending_bookings = all_bookings.exclude(status='COMPLETED')
    completed_bookings = all_bookings.filter(status='COMPLETED')
    
    # Get or create health profile
    health_profile, created = HealthProfile.objects.get_or_create(user=request.user)
    
    # Get active doctor access codes
    doctor_codes = DoctorAccessCode.objects.filter(
        user=request.user, 
        is_active=True, 
        expires_at__gt=datetime.now()
    ).order_by('-created_at')

    context = {
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'health_profile': health_profile,
        'doctor_codes': doctor_codes,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def health_profile_view(request):
    profile, created = HealthProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = HealthProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health profile updated successfully!')
            return redirect('users:dashboard')
    else:
        form = HealthProfileForm(instance=profile)
    
    return render(request, 'users/health_profile.html', {'form': form})

@login_required
def health_profile_setup(request):
    """Initial health profile setup after registration"""
    profile, created = HealthProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = HealthProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Welcome! Your health profile has been created.')
            return redirect('users:dashboard')
    else:
        form = HealthProfileForm(instance=profile)
    
    return render(request, 'users/health_profile_setup.html', {'form': form})

@login_required
def generate_doctor_code(request):
    if request.method == 'POST':
        form = DoctorAccessForm(request.POST)
        if form.is_valid():
            expires_at = datetime.now() + timedelta(days=int(form.cleaned_data['expires_in_days']))
            code = DoctorAccessCode.objects.create(
                user=request.user,
                doctor_name=form.cleaned_data['doctor_name'],
                expires_at=expires_at
            )
            messages.success(request, f'Doctor access code generated: {code.code}')
            return redirect('users:dashboard')
    else:
        form = DoctorAccessForm()
    
    return render(request, 'users/generate_doctor_code.html', {'form': form})

def doctor_access_view(request, code):
    access_code = get_object_or_404(DoctorAccessCode, code=code, is_active=True, expires_at__gt=datetime.now())
    user_bookings = Booking.objects.filter(user=access_code.user, status='COMPLETED').order_by('-created_at')
    
    context = {
        'access_code': access_code,
        'user_bookings': user_bookings,
        'health_profile': access_code.user.healthprofile if hasattr(access_code.user, 'healthprofile') else None,
    }
    return render(request, 'users/doctor_access.html', context)

