from django.contrib import admin
from .models import Project
from django.utils.html import format_html

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumbnail', 'area', 'investor', 'product', 'created_at')
    search_fields = ('name', 'investor', 'product')
    list_filter = ('created_at',)

    def thumbnail(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" width="80" height="50" style="object-fit: cover;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="80" height="50" style="object-fit: cover;" />', obj.image_url)
        return "-"
    thumbnail.short_description = "Ảnh"
