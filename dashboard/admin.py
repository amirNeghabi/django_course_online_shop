# dashboard/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# مدل‌های support
from support.models import Ticket, TicketMessage, TicketCategory

class DashboardAdminSite(admin.AdminSite):
    site_header = 'پنل مدیریت فروشگاه'
    site_title = 'مدیریت فروشگاه'
    index_title = 'خوش آمدید به پنل مدیریت'
    
    def index(self, request, extra_context=None):
        from dashboard.views import admin_dashboard
        return admin_dashboard(request)

dashboard_admin = DashboardAdminSite(name='dashboard_admin')


# -------------------------------
# Support Models در داشبورد
# -------------------------------

@admin.register(TicketCategory, site=dashboard_admin)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Ticket, site=dashboard_admin)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'category', 'status', 'created_at', 'updated_at', 'view_messages_link')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('subject', 'user__username', 'messages__message')
    readonly_fields = ('created_at', 'updated_at')
    
    def view_messages_link(self, obj):
        url = reverse('admin:ticketmessage_changelist') + f'?ticket__id__exact={obj.id}'
        return format_html('<a href="{}">مشاهده پیام‌ها</a>', url)
    view_messages_link.short_description = 'پیام‌ها'

@admin.register(TicketMessage, site=dashboard_admin)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'is_admin', 'short_message', 'created_at')
    list_filter = ('is_admin', 'created_at')
    search_fields = ('message', 'sender__username', 'ticket__subject')
    readonly_fields = ('created_at',)
    
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'متن پیام'
