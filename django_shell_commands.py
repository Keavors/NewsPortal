# Файл: django_shell_commands.py
# Эти команды нужно выполнить в Django shell (python manage.py shell)

from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

# 1. Создать пользователей
user1 = User.objects.create_user(username='user1')
user2 = User.objects.create_user(username='user2')

# 2. Создать авторов
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# 3. Добавить категории
cat1 = Category.objects.create(name='Спорт')
cat2 = Category.objects.create(name='Политика')
cat3 = Category.objects.create(name='Образование')
cat4 = Category.objects.create(name='Технологии')

# 4. Создать статьи/новости
post1 = Post.objects.create(
    author=author1,
    post_type='article',
    title='Статья о спорте',
    text='Текст статьи о спорте...'
)
post1.categories.add(cat1, cat3)

post2 = Post.objects.create(
    author=author2,
    post_type='article',
    title='Статья о политике',
    text='Текст статьи о политике...'
)
post2.categories.add(cat2)

post3 = Post.objects.create(
    author=author1,
    post_type='news',
    title='Новость о технологиях',
    text='Текст новости о технологиях...'
)
post3.categories.add(cat4)

# 5. Создать комментарии
comment1 = Comment.objects.create(post=post1, user=user1, text='Комментарий 1')
comment2 = Comment.objects.create(post=post2, user=user2, text='Комментарий 2')
comment3 = Comment.objects.create(post=post3, user=user1, text='Комментарий 3')
comment4 = Comment.objects.create(post=post1, user=user2, text='Комментарий 4')

# 6. Лайки/дислайки
post1.like()        # +1
post1.like()        # +1 → итого 2
post3.dislike()     # -1

comment1.like()     # +1
comment2.dislike()  # -1

# 7. Обновить рейтинг авторов
author1.update_rating()
author2.update_rating()

# 8. Вывести лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
print(f'Лучший автор: {best_author.user.username}, рейтинг: {best_author.rating}')

# 9. Вывести лучшую статью
best_post = Post.objects.order_by('-rating').first()
print(f'Дата: {best_post.created_at}')
print(f'Автор: {best_post.author.user.username}')
print(f'Рейтинг: {best_post.rating}')
print(f'Заголовок: {best_post.title}')
print(f'Превью: {best_post.preview()}')

# 10. Вывести комментарии к лучшей статье
comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(f'Дата: {comment.created_at}')
    print(f'Пользователь: {comment.user.username}')
    print(f'Рейтинг: {comment.rating}')
    print(f'Текст: {comment.text}')
    print('---')