# orders/services.py

from django.utils import timezone
from django.db import transaction
from .models import Order
from item.models import Item


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(buyer, product_id):

        try:
            product = Item.objects.select_for_update().get(
                id=product_id,
                status='active'
            )
        except Item.DoesNotExist:
            raise ValueError("Item does not exist or has been sold")

        if product.seller == buyer:
            raise ValueError("You cannot order yourself")

        # 创建订单
        order = Order.objects.create(
            buyer=buyer,
            seller=product.seller,
            product=product,
            price=product.price,
            status='paid',
            paid_at=timezone.now()
        )

        # 更新商品状态
        product.status = 'sold'
        product.save()

        return order