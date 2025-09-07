# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
import logging

from tests.models import LabTest, TestPackage
from .models import Booking
from .cart import Cart
from .forms import AnonymousBookingForm

logger = logging.getLogger(__name__)

@require_POST
def cart_add(request, item_type, item_id):
    cart = Cart(request)
    if item_type == 'test':
        item = get_object_or_404(LabTest, id=item_id)
    else:
        item = get_object_or_404(TestPackage, id=item_id)
    cart.add(item=item, item_type=item_type)
    return redirect('bookings:cart_detail')

@require_POST
def cart_remove(request, item_type, item_id):
    cart = Cart(request)
    unique_id = f"{item_type}_{item_id}"
    cart.remove(unique_id)
    return redirect('bookings:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'bookings/cart_detail.html', {'cart': cart})

def checkout_view(request):
    cart = Cart(request)
    logger.info(f"Checkout view accessed. Cart length: {len(cart)}")
    
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Please add some tests first.")
        return redirect('tests:test_list')

    if request.method == 'POST':
        logger.info(f"POST request received. Data: {request.POST}")
        form = AnonymousBookingForm(request.POST)
        
        if form.is_valid():
            logger.info(f"Form is valid. Data: {form.cleaned_data}")
            try:
                # For now, we simulate successful payment by creating the booking directly
                booking_data = {
                    'total_price': cart.get_total_price(),
                    'status': 'PAID'
                }
                
                if request.user.is_authenticated:
                    booking_data['user'] = request.user
                else:
                    booking_data['age'] = form.cleaned_data['age']
                    booking_data['gender'] = form.cleaned_data['gender']
                
                booking = Booking.objects.create(**booking_data)
                logger.info(f"Booking created: {booking.booking_code}")

                # Add items from the cart to the booking
                for unique_id, item_data in cart.cart.items():
                    logger.info(f"Processing cart item: {unique_id} -> {item_data}")
                    # Extract item_id from unique_id (format: "type_id")
                    item_type, item_id = unique_id.split('_', 1)
                    item_id = int(item_id)
                    
                    if item_type == 'test':
                        booking.tests.add(item_id)
                        logger.info(f"Added test {item_id} to booking")
                    elif item_type == 'package':
                        package = TestPackage.objects.get(id=item_id)
                        booking.package = package
                        booking.save()
                        logger.info(f"Added package {item_id} to booking")
                
                cart.clear() # Clear the session cart
                logger.info("Cart cleared, redirecting to success page")
                
                # Redirect to a success page showing the unique code
                return redirect('bookings:booking_success', booking_code=booking.booking_code)
            except Exception as e:
                logger.error(f"Error creating booking: {str(e)}")
                # Add error message to form if booking creation fails
                form.add_error(None, f"An error occurred while processing your order: {str(e)}")
                messages.error(request, f"Error processing order: {str(e)}")
        else:
            logger.warning(f"Form is not valid. Errors: {form.errors}")
            messages.error(request, "Please correct the errors below.")
        # If form is not valid, it will fall through to render the form with errors
    else:
        form = AnonymousBookingForm()
        logger.info("GET request - displaying checkout form")

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