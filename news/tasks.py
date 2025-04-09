from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from datetime import datetime, timedelta
from celery.schedules import crontab


@shared_task
def weekly_digest():
    last_week = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(
        created_at__gte=last_week,
        post_type='news'
    )

    for user in User.objects.filter(subscribed_categories__isnull=False).distinct():
        categories = user.subscribed_categories.all()
        user_posts = posts.filter(categories__in=categories).distinct()

        if user_posts.exists():
            html_content = render_to_string('email/weekly_digest.html', {
                'user': user,
                'posts': user_posts,
            })

            msg = EmailMultiAlternatives(
                subject='Еженедельный дайджест новостей',
                body='',
                from_email='noreply@newsportal.com',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


# Настройка периодических задач
app.conf.beat_schedule = {
    'weekly-digest': {
        'task': 'news.tasks.weekly_digest',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Пн 8:00
    },
}


@shared_task
def send_notification(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.categories.all()
    subscribers = set()

    for category in categories:
        subscribers.update(category.subscribers.all())

    subject = f'Новая новость в категории: {", ".join([c.name for c in categories])}'

    for user in subscribers:
        html_content = render_to_string('email/news_notification.html', {
            'post': post,
            'user': user,
        })

        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email='noreply@newsportal.com',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()