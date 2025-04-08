from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories')

    def __str__(self):
        return self.name

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = sum(post.rating * 3 for post in self.post_set.all())
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        post_comments_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        self.rating = post_rating + comment_rating + post_comments_rating
        self.save()


class Post(models.Model):
    POST_TYPES = [('article', 'Статья'), ('news', 'Новость')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def clean(self):
        if self.post_type == 'news':
            user_posts_today = Post.objects.filter(
                author=self.author,
                created_at__date=timezone.now().date(),
                post_type='news'
            ).exclude(pk=self.pk).count()

            if user_posts_today >= 3:
                raise ValidationError('Нельзя публиковать более 3 новостей в сутки!')

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()