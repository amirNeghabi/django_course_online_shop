# support/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Ticket, TicketMessage, TicketCategory


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'ticket_count')
    search_fields = ('name', 'description')
    
    def ticket_count(self, obj):
        count = obj.tickets.count()
        return format_html(
            '<span style="background: #667eea; color: white; padding: 3px 10px; border-radius: 10px;">{}</span>',
            count
        )
    ticket_count.short_description = 'تعداد تیکت'


class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 0
    readonly_fields = ('sender', 'created_at', 'is_admin')
    fields = ('sender', 'message', 'is_admin', 'created_at')
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'subject_display',
        'user_display',
        'category_display',
        'status_badge',
        'messages_count',
        'created_display',
        'updated_display'
    )
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('subject', 'user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'user')
    date_hierarchy = 'created_at'
    inlines = [TicketMessageInline]
    
    fieldsets = (
        ('اطلاعات تیکت', {
            'fields': ('user', 'category', 'subject', 'status')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subject_display(self, obj):
        return format_html(
            '<strong style="color: #667eea;">{}</strong>',
            obj.subject[:50]
        )
    subject_display.short_description = 'موضوع'
    
    def user_display(self, obj):
        return format_html(
            '<span style="color: #2d3748;"><i class="fa fa-user"></i> {}</span>',
            obj.user.get_full_name() or obj.user.email
        )
    user_display.short_description = 'کاربر'
    
    def category_display(self, obj):
        if obj.category:
            return format_html(
                '<span style="background: #f3f4f6; padding: 4px 12px; border-radius: 8px;">{}</span>',
                obj.category.name
            )
        return '-'
    category_display.short_description = 'دسته‌بندی'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ed8936',
            'answered': '#48bb78',
            'closed': '#718096'
        }
        labels = {
            'pending': 'در حال بررسی',
            'answered': 'پاسخ داده شده',
            'closed': 'بسته شده'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">{}</span>',
            colors.get(obj.status, '#718096'),
            labels.get(obj.status, obj.status)
        )
    status_badge.short_description = 'وضعیت'
    
    def messages_count(self, obj):
        count = obj.messages.count()
        return format_html(
            '<span style="color: #667eea;"><i class="fa fa-comments"></i> {}</span>',
            count
        )
    messages_count.short_description = 'پیام‌ها'
    
    def created_display(self, obj):
        return obj.created_at.strftime('%Y/%m/%d %H:%M')
    created_display.short_description = 'تاریخ ایجاد'
    
    def updated_display(self, obj):
        return obj.updated_at.strftime('%Y/%m/%d %H:%M')
    updated_display.short_description = 'آخرین بروزرسانی'
    
    actions = ['mark_as_answered', 'mark_as_closed', 'mark_as_pending']
    
    def mark_as_answered(self, request, queryset):
        updated = queryset.update(status='answered')
        self.message_user(request, f'{updated} تیکت به وضعیت "پاسخ داده شده" تغییر کرد.')
    mark_as_answered.short_description = '✅ علامت‌گذاری به عنوان "پاسخ داده شده"'
    
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} تیکت بسته شد.')
    mark_as_closed.short_description = '🔒 بستن تیکت'
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} تیکت به وضعیت "در حال بررسی" برگشت.')
    mark_as_pending.short_description = '⏳ بازگشت به "در حال بررسی"'


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.sender:
            obj.sender = request.user
        super().save_model(request, obj, form, change)

    
    def ticket_link(self, obj):
        url = reverse('admin:support_ticket_change', args=[obj.ticket.id])
        return format_html(
            '<a href="{}" style="color: #667eea; font-weight: 600;">{}</a>',
            url,
            obj.ticket.subject[:30]
        )
    ticket_link.short_description = 'تیکت'
    
    def sender_display(self, obj):
        return format_html(
            '<span style="color: #2d3748;">{}</span>',
            obj.sender.get_full_name() or obj.sender.email
        )
    sender_display.short_description = 'فرستنده'
    
    def message_preview(self, obj):
        preview = obj.message[:80] + '...' if len(obj.message) > 80 else obj.message
        return format_html(
            '<span style="color: #718096;">{}</span>',
            preview
        )
    message_preview.short_description = 'پیام'
    
    def admin_badge(self, obj):
        if obj.is_admin:
            return format_html(
                '<span style="background: #667eea; color: white; padding: 3px 10px; border-radius: 8px; font-size: 11px;">👨‍💼 ادمین</span>'
            )
        return format_html(
            '<span style="background: #48bb78; color: white; padding: 3px 10px; border-radius: 8px; font-size: 11px;">👤 کاربر</span>'
        )
    admin_badge.short_description = 'نوع'
    
    def created_display(self, obj):
        return obj.created_at.strftime('%Y/%m/%d %H:%M')
    created_display.short_description = 'تاریخ'
