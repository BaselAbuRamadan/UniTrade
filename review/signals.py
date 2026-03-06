from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from .utils import recalc_item_rating

@receiver(post_save, sender=Review)
def review_saved(sender, instance, **kwargs):
    recalc_item_rating(instance.order.item)

@receiver(post_delete, sender=Review)
def review_deleted(sender, instance, **kwargs):
    recalc_item_rating(instance.order.item)