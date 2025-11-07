from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from videos.models import Video
import random

class Command(BaseCommand):
    help = "Создает тестовых пользователей и видео"

    def handle(self, *args, **options):
        self.stdout.write("Создание пользователей...")
        users = [User(username=f"user{i}") for i in range(10000)]
        User.objects.bulk_create(users, ignore_conflicts=True)

        self.stdout.write("Создание видео...")
        users = list(User.objects.all())
        videos = [
            Video(
                title=f"Video {i}",
                description=f"Description for video {i}",
                author=random.choice(users),
                is_published=True,
            )
            for i in range(100000)
        ]
        Video.objects.bulk_create(videos)
        self.stdout.write(self.style.SUCCESS("✅ Данные успешно созданы"))
