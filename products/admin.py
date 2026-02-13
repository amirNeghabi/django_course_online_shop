from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Product, Comment  # اضافه شد Comment

# ---------- ProductAdmin ----------
@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'price', 'active', 'is_featured', 'featured_order', 'datetime_created']
    list_filter = ['active', 'is_featured', 'datetime_created']
    search_fields = ['title', 'description', 'short_description']
    list_per_page = 25

    actions = ['make_featured', 'remove_featured']

    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} محصول به پرفروش‌ها اضافه شد.')
    make_featured.short_description = "✅ اضافه کردن به پرفروش‌ها"

    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} محصول از پرفروش‌ها حذف شد.')
    remove_featured.short_description = "❌ حذف از پرفروش‌ها"
# ---------- پایان ProductAdmin ----------

# ---------- CommentAdmin ----------
@admin.register(Comment)
class CommentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    """پنل مدیریت کامنت‌ها"""
    list_display = ['short_body', 'product_link', 'author_link', 'stars', 'active', 'datetime_created']
    list_filter = ['active', 'stars', 'datetime_created']
    search_fields = ['body', 'author__email', 'author__username', 'product__title']
    list_per_page = 25
    actions = ['make_active', 'make_inactive']

    # نمایش کوتاه متن برای لیست
    @admin.display(description='متن کامنت')
    def short_body(self, obj):
        return obj.body[:50] + ('...' if len(obj.body) > 50 else '')

    # لینک به محصول
    @admin.display(description='محصول')
    def product_link(self, obj):
        url = obj.product.get_absolute_url()
        return format_html('<a href="{}">{}</a>', url, obj.product.title)

    # لینک به نویسنده
    @admin.display(description='نویسنده')
    def author_link(self, obj):
        url = reverse('admin:accounts_customuser_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.get_full_name() or obj.author.email)

    # اکشن فعال کردن کامنت‌ها
    @admin.action(description='فعال کردن کامنت‌های انتخاب شده')
    def make_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f'{updated} کامنت فعال شد.')

    # اکشن غیرفعال کردن کامنت‌ها
    @admin.action(description='غیرفعال کردن کامنت‌های انتخاب شده')
    def make_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f'{updated} کامنت غیرفعال شد.')
# ---------- پایان CommentAdmin ----------
