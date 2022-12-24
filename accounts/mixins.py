# from django.conf import settings
# from twilio.rest import Client


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
        
        
from django.conf import settings
from twilio.rest import Client


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


# def send_otp_on_phone():
#         client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
#         message = client.messages.create(
#                      body='Hai nithin',
#                      from_='+186059626740',
#                      to= '+919605286269'
#                  )
#         print("NITHI")
#         # print(message.sid)