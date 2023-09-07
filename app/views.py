from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from . import app
from .utils import get_gpt_answer


@app.route('/', methods=['POST'])
def webhook():
    incoming_message = request.values.get('Body', '')
    print(incoming_message)
    outgoing_message = get_gpt_answer(incoming_message)
    print(outgoing_message)
    print(type(outgoing_message))
    response = MessagingResponse()
    response.message(outgoing_message)
    return str(response)
