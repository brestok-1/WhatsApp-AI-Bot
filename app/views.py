from flask import, request
from twilio.twiml.messaging_response import MessagingResponse
from . import app
from .utils import get_gpt_answer


@app.route('/', methods=['POST'])
def webhook():
    incoming_message = request.values.get('Body', '')
    user_id = request.values.get('')
    outgoing_message = get_gpt_answer(incoming_message, user_id)
    response = MessagingResponse()
    response.message(outgoing_message)
    return str(response)
