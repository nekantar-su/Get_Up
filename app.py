from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    number = request.form['From']
    message_body = request.form['Body']
    resp = MessagingResponse()

    if message_body.lower() == 'weather':
        resp.message("Its beautiful outside")

    if message_body.lower() == 'Nav':
        resp.message("You have the following options: \n 1: Type Weather to view the weather \n 2: Type a message to see your phone number and typed message \n 3: Type help to view options ")

    else:    
        # Add a message
        resp.message(f"Hello {number} you said {message_body}")

    return str(resp)





if __name__ == "__main__":
    app.run(debug=True)
