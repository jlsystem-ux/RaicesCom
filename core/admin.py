from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Resource, Event, UserProfile, ContactMessage, StaffProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'name_es')
    search_fields = ('name', 'name_en', 'name_es')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'title_en', 'title_es', 'description')
    date_hierarchy = 'created_at'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'online')
    list_filter = ('date', 'online')
    search_fields = ('title', 'title_en', 'title_es', 'description', 'location')
    date_hierarchy = 'date'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_language', 'country_of_origin')
    list_filter = ('preferred_language',)
    search_fields = ('user__username', 'user__email', 'country_of_origin')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

    actions = [mark_as_read, mark_as_unread]

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'phone', 'is_active', 'show_on_contact_page', 'display_order')
    list_filter = ('is_active', 'show_on_contact_page', 'created_at')
    search_fields = ('name', 'name_en', 'name_es', 'title', 'email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'name_en', 'name_es', 'title', 'title_en', 'title_es')
        }),
        (_('Biography'), {
            'fields': ('bio', 'bio_en', 'bio_es'),
            'classes': ('collapse',),
        }),
        (_('Contact Information'), {
            'fields': ('phone', 'email', 'whatsapp')
        }),
        (_('Social Media'), {
            'fields': ('facebook', 'twitter', 'linkedin'),
            'classes': ('collapse',),
        }),
        (_('Photo'), {
            'fields': ('photo',)
        }),
        (_('Display Settings'), {
            'fields': ('is_active', 'show_on_contact_page', 'display_order')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
