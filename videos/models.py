from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    name = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)
    total_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.name} ({self.owner})"




class VideoFile(models.Model):
    QUALITY_HD = "HD"
    QUALITY_FHD = "FHD"
    QUALITY_UHD = "UHD"
    QUALITY_CHOICES = [
    (QUALITY_HD, "HD (720p)"),
    (QUALITY_FHD, "Full HD (1080p)"),
    (QUALITY_UHD, "Ultra HD (4K)"),
    ]


    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="videos/")
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES)


    class Meta:
        unique_together = ("video", "quality")


    def __str__(self):
        return f"{self.video_id} - {self.quality}"




class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("video", "user")
        indexes = [models.Index(fields=["video", "user"]) ]


    def __str__(self):
        return f"{self.user_id} -> {self.video_id}"