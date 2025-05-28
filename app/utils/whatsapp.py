from twilio.rest import Client
from django.conf import settings

def send_whatsapp_message(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    from_whatsapp_number = f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}'
    to_whatsapp_number = f'whatsapp:{to_number}'
    
    client.messages.create(
        body=message,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
