from django.db import models
from django.contrib.auth.models import User
from item.models import Item
from order.models import Order

class Conversation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='conversations')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_conversations')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_conversations')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} - {self.seller.username} - {self.item.title}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username}"


class Notification(models.Model):
    NOTIFICATION_TYPE = [
        ('new_message', 'New Message'),
        ('new_order', 'New Order'),
        ('order_status', 'Order Status Update'),
        ('order_cancelled', 'Order Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_notifications')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE, default='new_message')
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class UserPresence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='presence')
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} last seen at {self.last_seen}'