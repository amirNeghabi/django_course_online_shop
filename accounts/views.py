from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from orders.models import Order  # اگر اپ سفارشات داری


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        user.phone = request.POST.get("phone", "")
        user.city = request.POST.get("city", "")
        user.address = request.POST.get("address", "")
        user.postal_code = request.POST.get("postal_code", "")
        user.save()

        messages.success(request, "اطلاعات شما با موفقیت ذخیره شد.")
        return redirect("accounts:profile")

    # اصلاح فیلد created به datetime_created
    orders = Order.objects.filter(user=user).order_by("-datetime_created")

    return render(request, "accounts/profile.html", {
        "user": user,
        "orders": orders,
    })