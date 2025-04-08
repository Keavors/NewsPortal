from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
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