import random, schedule, time
import requests
from twilio.rest import Client
import os

quotes = requests.get("https://type.fit/api/quotes").json()

def send_message(quotes_list):

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    quote = random.choice(quotes_list)
    #print(quote)

    client.messages.create(from_='+17278557240',
                            to='+19179601965',
                           body=f" Daily Reminder to Be Great: \n {quote['text']} \n By: {quote['author']} \n Great Day To Have A Day! - Niko"
                           )

# send a message in the morning
#schedule.every().day.at("10:45").do(send_message, quotes)
schedule.every(1).minutes.do(send_message,quotes)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(2)