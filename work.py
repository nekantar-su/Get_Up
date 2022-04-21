import os
from twilio.rest import Client
import random
import requests

quotes = requests.get("https://type.fit/api/quotes").json()

def send_message(quotes_list = quotes):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_number = os.environ['TWILIO_NUMBER']
    to_number = os.environ['TO_NUMBER']
    client = Client(account_sid, auth_token)

    quote = random.choice(quotes_list)

    client.messages.create(from_= twilio_number,
                            to= to_number,
                           body=f" Daily Reminder to Be Great: \n {quote['text']} \n By: {quote['author']} \n Great Day To Have A Day! - Niko"
                           )

send_message()