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
    # Add a message
    resp.message(f"Hello {number} you said {message_body}")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
