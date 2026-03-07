from django.db import models
from django.contrib.auth.models import User
from order.models import Order


class Payment(models.Model):
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    transaction_no = models.CharField(max_length=50, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    paid_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_no} - {self.status}"