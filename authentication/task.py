
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_registration_email(email):
    send_mail(
        'Welcome to musicians site',
        'Learn new skills with us',
        from_email = None,
        recipient_list=[email]
    )