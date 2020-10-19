from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from musicians_site.settings import EMAIL_HOST_USER


@shared_task
def send_registration_email(email, email_template, subject):
    mail = EmailMultiAlternatives(subject, render_to_string(email_template), EMAIL_HOST_USER, to=[email, ])
    mail.send()
