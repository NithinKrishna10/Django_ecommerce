# from django.conf import settings
# from twilio.rest import Client
from twilio.rest import Client
from django.conf import settings


def send_message():
    try:
        account_sid = 'AC1cb3556b8da7c50552bfa5acbe8136c0'
        auth_token = 'e08a6c38c2e9815753a5c3b8fd142442'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="Nithin supera",
            from_='+186059626740',
            to='+917736563119'
        )
    except:
        print('hai')
        
        print("NITHI")
#     print(message.sid)
# class MessageHandler:

#     phone_number = None
#     otp = None


#     def __init__(self, phone_number, otp) -> None:

#         self.phone_number = phone_number
#         self.otp = otp

#     def send_otp_on_phone(self):
#         client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
#         message = client.messages \
#                 .create(
#                      body=f'Hai nithin {self.otp} ',
#                      from_='+186059626740',
#                      to=self.phone_number
#                  )
#         print("NITHI")
#         # print(message.sid)


# class MessageHandler:
#     phone_number=None
#     otp=None
#     def __init__(self,phone_number,otp) -> None:
#         self.phone_number=phone_number
#         self.otp=otp
#     def send_otp_via_message(self):
#         client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
#         message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_PHONE_NUMBER}',to=f'{settings.COUNTRY_CODE}{self.phone_number}')
#     def send_otp_via_whatsapp(self):
#         client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
#         message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_WHATSAPP_NUMBER}',to=f'whatsapp:{settings.COUNTRY_CODE}{self.phone_number}')


def send_otp_on_phone():
        client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        message = client.messages.create(
                     body='Hai nithin',
                     from_='+186059626740',
                     to= '+917736563119'
                 )
        print("NITHI")
        # print(message.sid)

