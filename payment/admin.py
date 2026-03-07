from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction_no", "order", "user", "amount", "status", "created_time", "paid_time")
    list_filter = ("status", "created_time")
    search_fields = ("transaction_no", "order__order_id", "user__username")