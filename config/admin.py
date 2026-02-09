"""
سفارشی‌سازی پنل ادمین Django
این فایل در config/admin.py قرار می‌گیرد
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# تنظیمات عمومی پنل ادمین
admin.site.site_header = _('پنل مدیریت فروشگاه')
admin.site.site_title = _('مدیریت فروشگاه')
admin.site.index_title = _('خوش آمدید به پنل مدیریت')

# تغییر متن‌های پیش‌فرض
admin.site.empty_value_display = _('-')


# کلاس پایه برای همه Admin ها
class BaseAdmin(admin.ModelAdmin):
    """کلاس پایه برای همه ادمین‌ها با تنظیمات مشترک"""
    
    # تنظیمات مشترک
    save_on_top = True
    list_per_page = 25
    
    # استایل‌های CSS سفارشی
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)


# تابع برای ثبت خودکار همه مدل‌ها در ادمین
def auto_register_models(app_name, admin_class=None):
    """
    ثبت خودکار همه مدل‌های یک app در پنل ادمین
    
    استفاده:
    from config.admin import auto_register_models
    auto_register_models('your_app_name')
    """
    from django.apps import apps
    
    if admin_class is None:
        admin_class = BaseAdmin
    
    app_models = apps.get_app_config(app_name).get_models()
    
    for model in app_models:
        try:
            admin.site.register(model, admin_class)
        except admin.sites.AlreadyRegistered:
            pass
