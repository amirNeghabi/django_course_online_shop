from django.shortcuts import render
from django.views.generic import TemplateView

from products.models import Product
from orders.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # آخرین محصولات (8 تا)
        context['latest_products'] = Product.objects.filter(
            active=True
        ).order_by('-datetime_created')[:8]
        
        # آمار کلی برای hero
        context['total_products'] = Product.objects.filter(active=True).count()
        context['total_users'] = User.objects.count()
        context['total_orders'] = Order.objects.filter(is_paid=True).count()
        
        return context


class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.html'