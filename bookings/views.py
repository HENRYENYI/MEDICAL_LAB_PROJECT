# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from tests.models import LabTest, TestPackage
from .models import Booking
from .cart import Cart
from .forms import AnonymousBookingForm

@require_POST
def cart_add(request, item_type, item_id):
    cart = Cart(request)
    if item_type == 'test':
        item = get_object_or_404(LabTest, id=item_id)
    else:
        item = get_object_or_404(TestPackage, id=item_id)
    cart.add(item=item, item_type=item_type)
    return redirect('bookings:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'bookings/cart_detail.html', {'cart': cart})

def checkout_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('tests:test_list')

    if request.method == 'POST':
        form = AnonymousBookingForm(request.POST)
        if form.is_valid():
            # For now, we simulate successful payment by creating the booking directly
            booking = Booking.objects.create(
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                total_price=cart.get_total_price(),
                status='PAID' # Simulate successful payment
            )

            # Add items from the cart to the booking
            for item in cart:
                if item['type'] == 'test':
                    booking.tests.add(item['id'])
                elif item['type'] == 'package':
                    # Note: This simple logic assumes one package per booking
                    package = TestPackage.objects.get(id=item['id'])
                    booking.package = package
                    booking.save()
            
            cart.clear() # Clear the session cart
            
            # Redirect to a success page showing the unique code
            return redirect('bookings:booking_success', booking_code=booking.booking_code)
    else:
        form = AnonymousBookingForm()

    return render(request, 'bookings/checkout.html', {'form': form, 'cart': cart})

def booking_success(request, booking_code):
    booking = get_object_or_404(Booking, booking_code=booking_code)
    return render(request, 'bookings/booking_success.html', {'booking': booking})


def check_result_view(request):
    if request.method == 'POST':
        code = request.POST.get('booking_code', '').strip().upper()
        if code:
            # Check if a booking with this code exists
            booking = Booking.objects.filter(booking_code=code).first()
            if booking:
                return redirect('bookings:result_detail', booking_code=booking.booking_code)
        
        # If code is not found or empty, render the page again with an error
        return render(request, 'bookings/check_result.html', {'error': 'Invalid booking code.'})

    return render(request, 'bookings/check_result.html')


def result_detail_view(request, booking_code):
    booking = get_object_or_404(Booking, booking_code=booking_code)
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/result_detail.html', context)