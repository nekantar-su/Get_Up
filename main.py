import os
from twilio.rest import Client
import requests
import random
from requests.exceptions import HTTPError


quotes = requests.get("https://type.fit/api/quotes").json()
randQuote = random.choice(quotes)


message = client.messages \
                .create(
                     body= f" Daily Reminder to Be Great: {randQuote['text']} By: {randQuote['author']}",
                     from_='+17278557240',
                     to='+19179601965'
                 )

print(message.sid)