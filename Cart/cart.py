from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect


class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item, quantity=1, action=None):
        """
        Add a item to the cart or update its quantity.
        """
        item_id = str(item.id)
        if item_id in self.cart:
            self.cart[item_id]['quantity'] += quantity
        else:
            self.cart[item_id] = {
                'userid': self.request.user.id,
                'item_id': item.id,
                'name': item.name,
                'quantity': quantity,
                'price': str(item.price),
                'image_link': item.image_link
            }
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, item):
        """
        Remove a item from the cart.
        """
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def decrement(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            self.cart[item_id]['quantity'] -= 1
            if self.cart[item_id]['quantity'] <= 0:
                del self.cart[item_id]  # Xóa sản phẩm khi quantity giảm về 0 hoặc âm
            self.save()

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True