from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .tasks import send_notification
from .models import Post
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Post)
def invalidate_article_cache(sender, instance, **kwargs):
    if instance.post_type == 'article':
        # Удаляем кэш детальной страницы
        cache.delete(f'article_detail:{instance.id}')

        # Удаляем кэш списка статей
        cache.delete_pattern('*.articles.list.*')  # Для cache_page

        # Удаляем кэш связанных категорий
        for category in instance.categories.all():
            cache.delete(f'category_{category.id}_articles')


@receiver([post_save, post_delete], sender=Post)
def invalidate_cache(sender, instance, **kwargs):
    # Удаляем кэш для списка новостей
    cache.delete_pattern("*.views.decorators.cache.cache_page.*")

    # Удаляем кэш для детальной страницы
    cache.delete(f"news:detail:{instance.id}")


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type == 'news':
        send_notification.delay(instance.id)  # Асинхронный вызов
    if created:
        categories = instance.categories.all()
        subscribers = User.objects.filter(
            subscribed_categories__in=categories
        ).distinct()

        subject = instance.title

        for user in subscribers:
            html_content = render_to_string('email/notification.html', {
                'post': instance,
                'user': user,
            })

            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email='noreply@newportal.com',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

User = get_user_model()

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get(name='common')
        instance.groups.add(common_group)