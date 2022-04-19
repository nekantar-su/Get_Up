from flask import Flask, request, redirect
from twilio import twiml


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    # Start our TwiML response
    number = request.form['From']
    message_body = request.form['Body']
    resp = twiml.Response()
    # Add a message
    resp.message(f"Hello {number} you said {message_body}")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
