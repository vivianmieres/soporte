from django.core.mail import send_mail
from django.conf import settings

def send_sms_via_email(phone_number, carrier_gateway, message):
    to_address = f"+{phone_number}@{carrier_gateway}"
    send_mail(
        subject="",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_address],
        fail_silently=False,
    )