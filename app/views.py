from flask import request

from database import db_context
from . import app
from .gpt_utils import get_gpt_answer
from .models import User
from .radist_utils import send_answer


@app.route('/', methods=['POST'])
def webhook():
    event = request.json['event']
    print(event)
    incoming_message = event['message']['text']['text']
    user_id = event['contact_id']
    chat_id = event['chat_id']
    # gpt_answer = get_gpt_answer(incoming_message, user_id)
    send_answer('Hi', chat_id)
    return 'Hi'
