from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from product.models import Shoe


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, verbose_name='Address')
    phone_number = models.CharField(max_length=15, verbose_name='Phone Number', help_text='Enter a valid phone number.')
    email = models.EmailField(verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='pending', verbose_name='Status')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Total Amount')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def calculate_total(self):
        self.total_amount = sum(item.get_total() for item in self.order_items.all())
        self.save()



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE, verbose_name='Order')
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, verbose_name='Shoe')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity} x {self.shoe.name}"

    def get_total(self):
        return self.price * self.quantity


