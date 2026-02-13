from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def merge_cart_after_login(sender, request, user, **kwargs):
    """
    بعد از لاگین، سبد خرید session قبلی را حفظ می‌کند
    """
    old_cart = request.session.get('cart')

    if old_cart:
        request.session['cart'] = old_cart
        request.session.modified = True
