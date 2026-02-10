from django.urls import path

from .views import payment_process, payment_callback, payment_success, payment_failed

app_name = 'payment'

urlpatterns = [
    path('process/', payment_process, name='payment_process'),
    path('callback/', payment_callback, name='payment_callback'),
    path('success/', payment_success, name='payment_success'),
    path('failed/', payment_failed, name='payment_failed'),
]