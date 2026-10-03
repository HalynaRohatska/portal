from django.contrib import admin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at", "is_pinned", "is_published")
    list_filter = ("is_pinned", "is_published", "created_at")
    search_fields = ("title", "content")
    ordering = ("-is_pinned", "-created_at")
