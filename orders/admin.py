from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from jalali_date.admin import ModelAdminJalaliMixin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity', 'price', 'get_total_price']
    readonly_fields = ['get_total_price']
    extra = 0

    @admin.display(description=_('قیمت کل'))
    def get_total_price(self, obj):
        if obj.pk:
            total = obj.quantity * obj.price
            return format_html('<strong>{} تومان</strong>', f'{total:,}')
        return '-'


@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    list_display = [
        'id',
        'user_link',
        'full_name',
        'phone_number',
        'is_paid',
        'total_price_display',
        'items_count',
        'payment_status',
        'datetime_created_jalali',
    ]

    list_display_links = ['id', 'full_name']

    list_filter = [
        'is_paid',
    ]

    search_fields = [
        'id',
        'first_name',
        'last_name',
        'phone_number',
        'address',
        'user__email',
        'zarinpal_authority',
    ]

    list_editable = ['is_paid']

    list_per_page = 25
    ordering = ['-datetime_created']
    date_hierarchy = 'datetime_created'

    fieldsets = (
        (_('اطلاعات مشتری'), {
            'fields': ('user', 'first_name', 'last_name', 'phone_number')
        }),
        (_('آدرس و یادداشت'), {
            'fields': ('address', 'order_notes')
        }),
        (_('وضعیت پرداخت'), {
            'fields': ('is_paid', 'zarinpal_authority'),
        }),
        (_('تاریخ‌ها'), {
            'fields': ('datetime_created', 'datetime_modified'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['datetime_created', 'datetime_modified']
    inlines = [OrderItemInline]

    @admin.display(description=_('کاربر'), ordering='user')
    def user_link(self, obj):
        if not obj.user:
            return '-'
        url = reverse('admin:accounts_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    @admin.display(description=_('نام و نام خانوادگی'))
    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    @admin.display(description=_('مبلغ کل'), ordering='id')
    def total_price_display(self, obj):
        total = int(obj.get_total_price() or 0)
        color = '#28a745' if obj.is_paid else '#dc3545'
        return format_html(
            '<strong style="color:{}">{} تومان</strong>',
            color,
            f'{total:,}'
        )

    @admin.display(description=_('تعداد آیتم'))
    def items_count(self, obj):
        return obj.items.count()

    @admin.display(description=_('وضعیت پرداخت'))
    def payment_status(self, obj):
        if obj.is_paid:
            return format_html('<span style="color:green">✔ پرداخت شده</span>')
        return format_html('<span style="color:red">✘ پرداخت نشده</span>')

    @admin.display(description=_('تاریخ ثبت'))
    def datetime_created_jalali(self, obj):
        return obj.datetime_created.strftime('%Y/%m/%d - %H:%M')
