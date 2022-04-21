from flask import Flask,request
from flask_apscheduler import APScheduler
import random
import os
from twilio.rest import Client
import requests
from twilio.twiml.messaging_response import MessagingResponse
from helpers import lookup

app = Flask(__name__)
scheduler = APScheduler()

quotes = requests.get("https://type.fit/api/quotes").json()

@app.route("/")
def index():
    return "Welcome to the scheduler"

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


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    number = request.form['From']
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
        
    if 'stock' in incoming_msg:
        try:
            stock = incoming_msg.split(' ')[1]

            stock =lookup(stock)

            if stock == '' or stock == None:
                resp.message("Please enter a valid stock")
            else:
                resp.message(f"{stock['name']} is trading at ${stock['price']}!")

        except IndexError:
            resp.message("Please enter in correct format. IE: Stock APPL")
        


    elif 'nav' in incoming_msg:
        resp.message("You have the following options: \n 1: Type Weather to view the weather \n 2: Type a message to see your phone number and typed message \n 3: Type nav to view options \n 4: Enter a stock to see its price \n 5: Enter todo - followed by task to add to todo \n 6: Enter view to view ToDo list")

    elif 'todo' in incoming_msg:
        try:
            user_todo= incoming_msg.split('-')[1:]
            #if user_todo[0] == '':
            #    resp.message("Enter a todo")
            
            todoList.append(' '.join(user_todo))
            resp.message(f"ToDo added {' '.join(user_todo)}.")
            
        except IndexError:
            resp.message("Please enter in correct format. IE: Todo-Take out garbage")

    elif 'view' in incoming_msg:
        #need to create a database
        resp.message(f"Current ToDo as follows:{*todoList,} ")

    elif 'weather' in incoming_msg:
        weather_key=os.environ['WEATHER_KEY']
        try:
            city = incoming_msg.split(' ')[1]
            complete_url = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + weather_key + "&q=" + city + "&units=imperial"
            x = requests.get(complete_url).json()
            if x["cod"] != "404":
                # store the value of "main"
                # key in variable y
                y = x["main"]
 
                # store the value corresponding
                # to the "temp" key of y
                current_temperature = y["temp"]
                resp.message(f"Temperature (in fahrenheit) is {str(current_temperature)} degrees in {city}!")
            
            else:
                resp.message(f"{city} Not Found ")

        except IndexError:
            resp.message("Please enter correct format: IE: Weather Brooklyn")

    else:    
        # Add a message
        resp.message(f"Hello {number} you said {incoming_msg}")

    return str(resp)


if __name__ == '__main__':
    scheduler.add_job(id = "Scheduled task", func= send_message , trigger = 'interval', seconds = 30)
    scheduler.start()
    app.run()