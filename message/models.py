from django.db import models
from django.contrib.auth.models import User
from item.models import Item


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Sender'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='Receiver'
    )

    Item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Related Item'
    )

    content = models.TextField(
        verbose_name='Message Content'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Sent Time'
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name='Is Read'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'From {self.sender} to {self.receiver} at {self.created_at}'