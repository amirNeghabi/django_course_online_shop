from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from jalali_date.admin import ModelAdminJalaliMixin

from .models import Product, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['author', 'body', 'stars', 'active', 'datetime_created']
    readonly_fields = ['datetime_created']
    extra = 0


@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    list_display = [
        'id',
        'title',
        'price',                # ✅ اضافه شد
        'active',
        'datetime_created_jalali',
    ]

    list_display_links = ['id', 'title']

    list_filter = ['active']
    search_fields = ['title', 'description']
    list_editable = ['price', 'active']   # ✅ بدون ارور
    ordering = ['-datetime_created']
    date_hierarchy = 'datetime_created'

    readonly_fields = ['datetime_created', 'datetime_modified']
    inlines = [CommentInline]

    @admin.display(description=_('تاریخ ایجاد'))
    def datetime_created_jalali(self, obj):
        return obj.datetime_created.strftime('%Y/%m/%d - %H:%M')


@admin.register(Comment)
class CommentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    list_display = [
        'id',
        'product',
        'author',
        'stars',
        'active',
        'datetime_created_jalali',
    ]

    list_filter = ['active', 'stars']
    list_editable = ['active']
    ordering = ['-datetime_created']

    @admin.display(description=_('تاریخ ثبت'))
    def datetime_created_jalali(self, obj):
        return obj.datetime_created.strftime('%Y/%m/%d - %H:%M')
