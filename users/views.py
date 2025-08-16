

# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from bookings.models import Booking



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def dashboard_view(request):
    # Get bookings for the currently logged-in user
    all_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    pending_bookings = all_bookings.exclude(status='COMPLETED')
    completed_bookings = all_bookings.filter(status='COMPLETED')

    context = {
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
    }
    return render(request, 'users/dashboard.html', context)

