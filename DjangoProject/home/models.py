from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Items'
    def __str__(self):
        return self.name

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return f"{self.first_name} {self.last_name} {created_at_str}"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price
    def __str__(self):
        order_info = f"Order ID: {self.order.id}, Owner: {self.order.first_name} {self.order.last_name}, Created At: {self.order.created_at}"
        return f"Product: {self.product_name}, {order_info}"