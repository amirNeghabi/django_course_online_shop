from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from orders.models import Order


def payment_process(request):
    # به جای زرین‌پال → درگاه فیک
    return redirect("payment:fake_gateway")


def fake_gateway(request):
    return render(request, "payment/fake_gateway.html")


def fake_gateway_result(request, result):
    order_id = request.session.get("order_id")

    if not order_id:
        return redirect("cart:cart_detail")

    order = get_object_or_404(Order, id=order_id)

    if result == "success":
        order.is_paid = True
        order.save()

        del request.session["order_id"]

        messages.success(request, "پرداخت با موفقیت انجام شد.")
        return redirect("payment:payment_success")

    messages.error(request, "پرداخت ناموفق بود.")
    return redirect("payment:payment_failed")


def payment_callback(request):
    pass


def payment_success(request):
    return render(request, "payment/payment_success.html")


def payment_failed(request):
    return render(request, "payment/payment_failed.html")
