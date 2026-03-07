from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("<int:order_id>/", views.pay_order, name="pay_order"),
    path("<int:order_id>/confirm/", views.pay_confirm, name="pay_confirm"),
    path("<int:order_id>/success/", views.pay_success, name="pay_success"),
]