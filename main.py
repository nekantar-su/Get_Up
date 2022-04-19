import os
from twilio.rest import Client
import requests
import random
from requests.exceptions import HTTPError


quotes = requests.get("https://type.fit/api/quotes").json()
randQuote = random.choice(quotes)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body= f" Daily Reminder to Be Great: {randQuote['text']} By: {randQuote['author']}",
                     from_='+17278557240',
                     to='+19179601965'
                 )

print(message.sid)