from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


class DashboardAdminSite(admin.AdminSite):
    site_header = 'پنل مدیریت فروشگاه'
    site_title = 'مدیریت فروشگاه'
    index_title = 'خوش آمدید به پنل مدیریت'
    
    def index(self, request, extra_context=None):
        from dashboard.views import admin_dashboard
        return admin_dashboard(request)