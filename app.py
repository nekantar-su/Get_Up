import random, schedule, time
import requests
from twilio.rest import Client
import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
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

@app.route("/")
def index():
# send a message in the morning
#schedule.every().day.at("10:45").do(send_message, quotes)
    schedule.every(1).minutes.do(send_message,quotes)
    
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(2)
    #return "Hello World!"



@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    number = request.form['From']
    message_body = request.form['Body']
    resp = MessagingResponse()

    #if message_body.lower() == 'motivation':


    if message_body.lower() == 'weather':
        resp.message("Its beautiful outside")

    elif message_body.lower() == 'nav':
        resp.message("You have the following options: \n 1: Type Weather to view the weather \n 2: Type a message to see your phone number and typed message \n 3: Type nav to view options ")

    else:    
        # Add a message
        resp.message(f"Hello {number} you said {message_body}")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)