from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from orders.models import Order

def payment_process(request):
    """
    شروع فرآیند پرداخت (درگاه فیک)
    """
    order_id = request.session.get("order_id")
    if not order_id:
        messages.warning(request, "سفارشی برای پرداخت پیدا نشد.")
        return redirect("product_list")
    
    return redirect("payment:fake_gateway")


def fake_gateway(request):
    """
    صفحه شبیه‌سازی درگاه پرداخت
    """
    return render(request, "payment/fake_gateway.html")


def fake_gateway_result(request, result):
    """
    نتیجه پرداخت فیک: success یا failed
    """
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


def payment_success(request):
    """
    صفحه پرداخت موفق
    """
    return render(request, "payment/payment_success.html")


def payment_failed(request):
    """
    صفحه پرداخت ناموفق با امکان پرداخت مجدد
    """
    order_id = request.session.get("order_id")
    order = None
    if order_id:
        order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "payment/payment_failed.html", {"order": order})


def retry_payment(request, order_id):
    """
    پرداخت مجدد برای سفارش‌هایی که قبلاً پرداخت نشدند
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.is_paid:
        # اگر سفارش قبلاً پرداخت شده، مستقیم به جزئیات سفارش
        messages.info(request, "این سفارش قبلاً پرداخت شده است.")
        return redirect("orders:order_detail", pk=order.id)

    # ذخیره order_id در session برای استفاده در payment_process
    request.session["order_id"] = order.id
    return redirect("payment:payment_process")


def payment_callback(request):
    """
    این ویو برای درگاه واقعی لازم است
    """
    pass
