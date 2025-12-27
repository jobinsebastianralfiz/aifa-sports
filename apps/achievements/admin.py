from django.contrib import admin
from .models import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'category', 'is_active', 'is_featured', 'show_on_homepage']
    list_filter = ['category', 'is_active', 'is_featured', 'year']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['display_order', '-year']
