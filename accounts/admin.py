from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Sum
from jalali_date.admin import ModelAdminJalaliMixin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdminJalaliMixin, UserAdmin):
    """پنل مدیریت کاربران"""
    
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    
    # لیست نمایش
    list_display = [
        'email',
        'username',
        'full_name',
        'is_active_display',
        'is_staff_display',
        'orders_count',
        'total_spent',
        'date_joined_display',
    ]
    
    # فیلدهایی که قابل کلیک هستند
    list_display_links = ['email', 'username']
    
    # فیلترها
    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined',
    ]
    
    # جستجو
    search_fields = ['email', 'username', 'first_name', 'last_name']
    
    # ویرایش مستقیم
    list_editable = []
    
    # تعداد در صفحه
    list_per_page = 25
    
    # ترتیب پیش‌فرض
    ordering = ['-date_joined']
    
    # تاریخ‌های سلسله مراتبی
    date_hierarchy = 'date_joined'
    
    # اکشن‌ها
    actions = ['activate_users', 'deactivate_users', 'make_staff']
    
    # فیلدها در فرم (برای ویرایش)
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        (_('اطلاعات شخصی'), {
            'fields': ('first_name', 'last_name')
        }),
        (_('دسترسی‌ها'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('تاریخ‌های مهم'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
        (_('آمار کاربر'), {
            'fields': ('get_user_statistics',),
            'classes': ('collapse',)
        }),
    )
    
    # فیلدها در فرم (برای افزودن)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
        (_('اطلاعات شخصی'), {
            'fields': ('first_name', 'last_name')
        }),
        (_('دسترسی‌ها'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined', 'get_user_statistics']
    
    # متدهای سفارشی
    @admin.display(description=_('نام و نام خانوادگی'))
    def full_name(self, obj):
        """نمایش نام کامل"""
        if obj.first_name or obj.last_name:
            return f'{obj.first_name} {obj.last_name}'.strip()
        return format_html('<span style="color: #999;">-</span>')
    
    @admin.display(description=_('وضعیت'), boolean=True, ordering='is_active')
    def is_active_display(self, obj):
        """نمایش وضعیت فعال/غیرفعال"""
        return obj.is_active
    
    @admin.display(description=_('کارمند'), boolean=True, ordering='is_staff')
    def is_staff_display(self, obj):
        """نمایش وضعیت کارمند"""
        return obj.is_staff
    
    @admin.display(description=_('تعداد سفارشات'))
    def orders_count(self, obj):
        """تعداد سفارشات کاربر"""
        from orders.models import Order
        count = Order.objects.filter(user=obj).count()
        if count > 0:
            url = reverse('admin:orders_order_changelist') + f'?user__id__exact={obj.id}'
            return format_html(
                '<a href="{}" style="color: #007bff;">{} سفارش</a>',
                url, count
            )
        return format_html('<span style="color: #999;">0 سفارش</span>')
    
    @admin.display(description=_('مجموع خرید'))
    def total_spent(self, obj):
        """مجموع مبلغ خرید کاربر"""
        from orders.models import Order
        orders = Order.objects.filter(user=obj, is_paid=True)
        
        if orders.exists():
            total = sum(order.get_total_price() for order in orders)
            color = '#28a745' if total > 1000000 else '#007bff'
            return format_html(
                '<strong style="color: {};">{:,} تومان</strong>',
                color, total
            )
        return format_html('<span style="color: #999;">0 تومان</span>')
    
    @admin.display(description=_('تاریخ عضویت'))
    def date_joined_display(self, obj):
        """نمایش تاریخ عضویت"""
        return obj.date_joined.strftime('%Y/%m/%d')
    
    @admin.display(description=_('آمار کاربر'))
    def get_user_statistics(self, obj):
        """نمایش آمار کامل کاربر"""
        if not obj.pk:
            return '-'
        
        from orders.models import Order
        from products.models import Comment
        
        total_orders = Order.objects.filter(user=obj).count()
        paid_orders = Order.objects.filter(user=obj, is_paid=True).count()
        total_spent = sum(
            order.get_total_price() 
            for order in Order.objects.filter(user=obj, is_paid=True)
        )
        total_comments = Comment.objects.filter(author=obj).count()
        
        html = '<div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">'
        html += f'<h3 style="margin-top: 0;">آمار {obj.email}</h3>'
        html += '<table style="width: 100%;">'
        html += f'<tr><td><strong>کل سفارشات:</strong></td><td>{total_orders}</td></tr>'
        html += f'<tr><td><strong>سفارشات پرداخت شده:</strong></td><td>{paid_orders}</td></tr>'
        html += f'<tr><td><strong>مجموع خرید:</strong></td><td style="color: #28a745;"><strong>{total_spent:,} تومان</strong></td></tr>'
        html += f'<tr><td><strong>تعداد نظرات:</strong></td><td>{total_comments}</td></tr>'
        html += f'<tr><td><strong>آخرین ورود:</strong></td><td>{obj.last_login.strftime("%Y/%m/%d %H:%M") if obj.last_login else "هرگز"}</td></tr>'
        html += '</table></div>'
        
        return format_html(html)
    
    # اکشن‌های سفارشی
    @admin.action(description=_('فعال کردن کاربران انتخاب شده'))
    def activate_users(self, request, queryset):
        """فعال کردن دسته‌جمعی کاربران"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} کاربر فعال شد.')
    
    @admin.action(description=_('غیرفعال کردن کاربران انتخاب شده'))
    def deactivate_users(self, request, queryset):
        """غیرفعال کردن دسته‌جمعی کاربران"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} کاربر غیرفعال شد.')
    
    @admin.action(description=_('تبدیل به کارمند'))
    def make_staff(self, request, queryset):
        """تبدیل کاربران به کارمند"""
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} کاربر به کارمند تبدیل شد.')
