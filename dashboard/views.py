from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from products.models import Product
from accounts.models import CustomUser


@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    
    total_revenue = 0
    for order in Order.objects.filter(is_paid=True):
        total_revenue += order.get_total_price()
    
    total_users = CustomUser.objects.count()
    total_products = Product.objects.count()
    
    recent_orders = Order.objects.select_related('user').order_by('-datetime_created')[:5]
    recent_products = Product.objects.order_by('-datetime_created')[:5]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_products': total_products,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
    }
    
    return render(request, 'admin/index.html', context)