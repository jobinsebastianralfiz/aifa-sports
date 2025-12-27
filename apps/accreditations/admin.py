from django.contrib import admin
from .models import Accreditation


@admin.register(Accreditation)
class AccreditationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_body', 'accreditation_type', 'is_active', 'is_featured', 'show_on_homepage']
    list_filter = ['accreditation_type', 'is_active', 'is_featured']
    search_fields = ['name', 'issuing_body', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order']
