from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import NewsletterSubscription

@shared_task
def send_newsletter():
    subscribers = NewsletterSubscription.objects.all()
    recipients = [subscriber.email for subscriber in subscribers]
    send_mail(
        'Новини від магазину',
        'Це тестове повідомлення про новини від магазину',
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=False,
    )
