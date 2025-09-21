from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Category, Resource, Event, UserProfile, ContactMessage, StaffProfile, BlogCategory, BlogPost, Testimonial

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

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'color_preview', 'icon')
    list_editable = ('color', 'icon')
    search_fields = ('name', 'name_en', 'name_es')
    prepopulated_fields = {'slug': ('name',)}

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = _('Color Preview')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'category', 'author', 'is_published', 'is_featured', 'published_date')
    list_filter = ('post_type', 'category', 'is_published', 'is_featured', 'published_date', 'created_at')
    search_fields = ('title', 'title_en', 'title_es', 'summary', 'content')
    readonly_fields = ('created_at', 'updated_at', 'reading_time_display')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'title_en', 'title_es', 'slug', 'post_type', 'category')
        }),
        (_('Content'), {
            'fields': ('summary', 'summary_en', 'summary_es', 'content', 'content_en', 'content_es')
        }),
        (_('Media'), {
            'fields': ('featured_image',)
        }),
        (_('Publishing'), {
            'fields': ('author', 'is_published', 'is_featured', 'published_date')
        }),
        (_('SEO'), {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
        (_('Metadata'), {
            'fields': ('reading_time', 'reading_time_display', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def reading_time_display(self, obj):
        return f"{obj.get_reading_time()} minutes"
    reading_time_display.short_description = _('Estimated Reading Time')

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new post
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def publish_posts(self, request, queryset):
        queryset.update(is_published=True)
    publish_posts.short_description = _("Publish selected posts")

    def unpublish_posts(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_posts.short_description = _("Unpublish selected posts")

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = _("Mark as featured")

    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
    remove_featured.short_description = _("Remove featured status")

    actions = [publish_posts, unpublish_posts, make_featured, remove_featured]

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_of_origin', 'is_featured', 'is_published', 'consent_given', 'created_at')
    list_filter = ('is_featured', 'is_published', 'consent_given', 'country_of_origin', 'created_at')
    search_fields = ('name', 'country_of_origin', 'content')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Personal Information'), {
            'fields': ('name', 'country_of_origin', 'photo')
        }),
        (_('Testimonial Content'), {
            'fields': ('content', 'content_en', 'content_es')
        }),
        (_('Publishing Settings'), {
            'fields': ('is_featured', 'is_published', 'consent_given')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def publish_testimonials(self, request, queryset):
        queryset.update(is_published=True)
    publish_testimonials.short_description = _("Publish selected testimonials")

    def unpublish_testimonials(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_testimonials.short_description = _("Unpublish selected testimonials")

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = _("Mark as featured")

    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
    remove_featured.short_description = _("Remove featured status")

    actions = [publish_testimonials, unpublish_testimonials, make_featured, remove_featured]
