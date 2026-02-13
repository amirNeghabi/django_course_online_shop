# dashboard/views.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from products.models import Product
from accounts.models import CustomUser
from support.models import Ticket  # اضافه شده

@staff_member_required
def admin_dashboard(request):
    # -------------------------
    # آمار سفارش‌ها، کاربران، محصولات
    # -------------------------
    total_orders = Order.objects.count()
    total_revenue = sum(order.get_total_price() for order in Order.objects.filter(is_paid=True))
    total_users = CustomUser.objects.count()
    total_products = Product.objects.count()
    
    recent_orders = Order.objects.select_related('user').order_by('-datetime_created')[:5]
    recent_products = Product.objects.order_by('-datetime_created')[:5]
    
    # -------------------------
    # آمار تیکت‌ها
    # -------------------------
    total_tickets = Ticket.objects.count()
    tickets_pending = Ticket.objects.filter(status='pending').count()
    tickets_answered = Ticket.objects.filter(status='answered').count()
    tickets_closed = Ticket.objects.filter(status='closed').count()
    
    recent_tickets = Ticket.objects.select_related('user', 'category').order_by('-created_at')[:5]
    
    context = {
        # آمار فعلی
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_products': total_products,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
        
        # آمار تیکت‌ها
        'total_tickets': total_tickets,
        'tickets_pending': tickets_pending,
        'tickets_answered': tickets_answered,
        'tickets_closed': tickets_closed,
        'recent_tickets': recent_tickets,
    }
    
    return render(request, 'admin/index.html', context)
