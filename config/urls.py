"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Override admin index
def custom_admin_index(self, request, extra_context=None):
    from orders.models import Order
    from products.models import Product
    from accounts.models import CustomUser
    
    total_orders = Order.objects.count()
    total_revenue = sum(order.get_total_price() for order in Order.objects.filter(is_paid=True))
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
    
    from django.shortcuts import render
    return render(request, 'admin/index.html', context)

admin.site.index = custom_admin_index.__get__(admin.site, admin.AdminSite)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('allauth.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('orders.urls')),
    path('payment/', include('payment.urls')),

    # Rosetta (i18n)
    path('rosetta/', include('rosetta.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)