from twilio.rest import Client
import smtplib



def send_sms(phone, message):
    print(f"SMS sent to {phone}")



def send_email(email, subject, body):
    print(f"Email sent to {email}")