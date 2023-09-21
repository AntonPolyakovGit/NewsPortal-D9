from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from django.conf import settings
from .models import PostCategory, Post, Category, Comment

def send_notifications (preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email= settings.DEFAULT_FROM_EMAIL,
        to= subscribers
    )
    print(subscribers)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post (sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers: list = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

