from django.core.management import BaseCommand
from django.contrib.auth.models import User
from news.models import Author, Post

class Command(BaseCommand):
    help = "Создаёт тестовые новости и статьи"

    def handle(self, *args, **options):
        # Создаём пользователя и автора
        user = User.objects.create_user(username='test_author')
        author = Author.objects.create(user=user)

        # Создаём новости
        Post.objects.create(
            author=author,
            title="Тестовая новость 1",
            text="Это текст новости 1. Редиска!",
            post_type='news'
        )

        Post.objects.create(
            author=author,
            title="Тестовая новость 2",
            text="Это текст новости 2. Хрен!",
            post_type='news'
        )

        self.stdout.write(self.style.SUCCESS('Данные созданы!'))