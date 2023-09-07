from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from . import app


@app.route('/', methods=['POST'])
def webhook():
    incoming_message = request.values.get('Body', '')
    outgoing_message = incoming_message + '.'

    response = MessagingResponse()
    response.message(outgoing_message)
    return str(response)
