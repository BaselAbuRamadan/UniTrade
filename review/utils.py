from django.db.models import Avg, Count, Sum
from .models import Review

def recalc_item_rating(item):
    qs = Review.objects.filter(order__item=item)
    agg = qs.aggregate(
        s=Sum("rating"),
        c=Count("id"),
        a=Avg("rating")
    )
    item.rating_sum = agg["s"] or 0
    item.rating_count = agg["c"] or 0
    item.rating_avg = agg["a"] or 0
    item.save(update_fields=["rating_sum", "rating_count", "rating_avg"])