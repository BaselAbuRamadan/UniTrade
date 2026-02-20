from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Item


@receiver(pre_delete, sender=User)
def handle_user_delete(sender, instance, **kwargs):
    policy = getattr(settings, "USER_DELETE_ITEM_POLICY", "delist")
    new_status = Item.Status.HIDDEN if policy == "hide" else Item.Status.DELISTED
    Item.objects.filter(seller=instance).update(status=new_status, seller=None)