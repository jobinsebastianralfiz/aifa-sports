from django.contrib import admin
from .models import Facility, FacilityCategory


@admin.register(FacilityCategory)
class FacilityCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'area_size', 'is_featured', 'show_on_homepage', 'display_order']
    list_filter = ['category', 'is_featured', 'show_on_homepage', 'is_active']
    list_editable = ['is_featured', 'show_on_homepage', 'display_order']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
