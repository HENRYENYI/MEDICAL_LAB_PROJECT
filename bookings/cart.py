# bookings/cart.py
from decimal import Decimal
from django.conf import settings
from tests.models import LabTest, TestPackage

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item, item_type):
        item_id = str(item.id)
        unique_id = f"{item_type}_{item_id}"
        if unique_id not in self.cart:
            self.cart[unique_id] = {'price': str(item.price), 'type': item_type, 'name': item.name}
        self.save()

    def save(self):
        self.session.modified = True
        
    def __iter__(self):
        for unique_id, item_data in self.cart.items():
            item_data['price'] = Decimal(item_data['price'])
            yield item_data
            
    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()