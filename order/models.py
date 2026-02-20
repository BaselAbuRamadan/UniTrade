from django.db import models
from django.contrib.auth.models import User
from item.models import Item


class Order(models.Model):
    ORDER_STATUS = [
        'pending',
        'paid',
        'completed',
        'cancelled',
    ]

    order_number = models.CharField(max_length=20, unique=True, verbose_name='Order Number')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_as_buyer', verbose_name='Buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_as_seller', verbose_name='Seller')
    Item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Item')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Dealt Price', default=0)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending', verbose_name='Order Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Order Created Time')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Order Paid Time')