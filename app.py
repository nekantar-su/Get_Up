from flask import Flask,request
from flask_apscheduler import APScheduler
import random
import os
from twilio.rest import Client
import requests
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)
scheduler = APScheduler()
quotes = requests.get("https://type.fit/api/quotes").json()
todoList = []

@app.route("/")
def index():
    return "Welcome to the scheduler"

def send_message(quotes_list = quotes):
    print("started")
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    quote = random.choice(quotes_list)
    print(quote)

    client.messages.create(from_='+17278557240',
                            to='+19179601965',
                           body=f" Daily Reminder to Be Great: \n {quote['text']} \n By: {quote['author']} \n Great Day To Have A Day! - Niko"
                           )
    print("reached")


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    number = request.form['From']
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()

    if 'weather' in incoming_msg:
        resp.message("Its beautiful outside")

    if 'stock' in incoming_msg:
        try:
            stock = incoming_msg.split(' ')[1]
            resp.message(f"Stock wanted is {stock}")
        except IndexError:
            resp.message("Please enter in correct format. IE: Stock APPL")

    elif 'nav' in incoming_msg:
        resp.message("You have the following options: \n 1: Type Weather to view the weather \n 2: Type a message to see your phone number and typed message \n 3: Type nav to view options ")

    else:    
        # Add a message
        resp.message(f"Hello {number} you said {incoming_msg}")

    return str(resp)



if __name__ == '__main__':
    #scheduler.add_job(id = "Scheduled task", func= send_message , trigger = 'interval', seconds = 30)
    #scheduler.start()
    app.run()