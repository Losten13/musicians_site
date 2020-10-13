from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_registration_email(email, template, subject):
    mail = EmailMultiAlternatives(subject, render_to_string(template), to=[email, ])
    mail.send()
