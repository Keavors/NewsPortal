from django.core.management import BaseCommand
from news.models import *


class Command(BaseCommand):
    help = "Create test data"

    def handle(self, *args, **options):
        user = User.objects.create_user(username='testuser')
        author = Author.objects.create(user=user)
        category = Category.objects.create(name='Тестовая категория')

        post = Post.objects.create(
            author=author,
            post_type='news',
            title='Тестовая новость',
            text='Содержание новости'
        )
        post.categories.add(category)

        self.stdout.write("Тестовые данные созданы")

# run: python manage.py create_test_data