from django.urls import path
from .views import (
    payment_process,
    payment_callback,
    payment_success,
    payment_failed,
    fake_gateway,
    fake_gateway_result,
)

app_name = "payment"

urlpatterns = [
    path("process/", payment_process, name="payment_process"),
    path("callback/", payment_callback, name="payment_callback"),

    # 👇 درگاه فیک
    path("fake/", fake_gateway, name="fake_gateway"),
    path("fake/result/<str:result>/", fake_gateway_result, name="fake_result"),

    path("success/", payment_success, name="payment_success"),
    path("failed/", payment_failed, name="payment_failed"),
]
