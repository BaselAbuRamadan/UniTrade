from django.db import models
from django.conf import settings
from order.models import Order


class Review(models.Model):

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveSmallIntegerField(default=5)
    content = models.TextField(blank=True)
    share_token = models.CharField(max_length=64, blank=True, null=True, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review {self.id} - {self.rating} stars"


class ReviewReport(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="reports")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'reporter')


class ReviewImage(models.Model):
    review = models.ForeignKey("Review", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="review_images/")
    uploaded_time = models.DateTimeField(auto_now_add=True)

class ReviewLike(models.Model):
    review = models.ForeignKey("Review", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("review", "user")