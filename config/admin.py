"""
سفارشی‌سازی پنل ادمین Django
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# تابع برای اضافه کردن داده‌های داشبورد به context
def get_admin_context():
    from products.models import Product
    from orders.models import Order
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # آمار کلی
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_products = Product.objects.filter(active=True).count()
    
    # محاسبه مجموع فروش
    total_revenue = 0
    for order in Order.objects.filter(is_paid=True):
        total_revenue += order.get_total_price()
    
    # آخرین سفارشات و محصولات
    recent_orders = Order.objects.select_related('user').order_by('-datetime_created')[:5]
    recent_products = Product.objects.order_by('-datetime_created')[:5]
    
    return {
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
    }


# Override AdminSite
class CustomAdminSite(admin.AdminSite):
    site_header = 'پنل مدیریت فروشگاه'
    site_title = 'مدیریت فروشگاه'
    index_title = 'خوش آمدید به پنل مدیریت'
    
    def each_context(self, request):
        context = super().each_context(request)
        # اضافه کردن داده‌های سفارشی فقط برای صفحه اصلی
        if request.path == '/admin/' or request.path == '/admin':
            context.update(get_admin_context())
        return context


# جایگزین کردن admin site پیش‌فرض
admin.site = CustomAdminSite()
admin.sites.site = admin.site
