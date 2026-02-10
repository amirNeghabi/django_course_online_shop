from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render


admin.site.site_header = _('پنل مدیریت فروشگاه')
admin.site.site_title = _('مدیریت فروشگاه')
admin.site.index_title = _('خوش آمدید به پنل مدیریت')
admin.site.empty_value_display = _('-')


def custom_index(self, request, extra_context=None):
    from orders.models import Order
    from products.models import Product
    from accounts.models import CustomUser
    
    total_orders = Order.objects.count()
    
    total_revenue = 0
    for order in Order.objects.filter(is_paid=True):
        total_revenue += order.get_total_price()
    
    total_users = CustomUser.objects.count()
    total_products = Product.objects.count()
    
    recent_orders = Order.objects.select_related('user').order_by('-datetime_created')[:5]
    recent_products = Product.objects.order_by('-datetime_created')[:5]
    
    context = {
        **self.each_context(request),
        'title': self.index_title,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_products': total_products,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
    }
    
    if extra_context:
        context.update(extra_context)
    
    return render(request, 'admin/index.html', context)


admin.site.index = custom_index.__get__(admin.site, admin.AdminSite)


class BaseAdmin(admin.ModelAdmin):
    save_on_top = True
    list_per_page = 25
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)