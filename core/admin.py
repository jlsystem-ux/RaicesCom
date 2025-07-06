from django.contrib import admin
from .models import Category, Resource, Event, UserProfile

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
