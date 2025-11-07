from django.contrib import admin
from .models import Video, VideoFile, Like


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "is_published", "total_likes", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("name", "owner__username")




@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = ("id", "video", "quality")




@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "video", "user", "created_at")