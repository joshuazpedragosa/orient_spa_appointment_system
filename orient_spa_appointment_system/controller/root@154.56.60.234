from twilio.rest import Client
from django.conf import settings

def send_sms(message, to):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to
        )
        return True  
    except Exception as e:
        print(str(e))
        return False  
