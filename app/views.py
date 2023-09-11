from flask import request

from database import redis
from .tasks import get_gpt_answer


def webhook():
    event = request.json['event']
    incoming_message = event['message']['text']['text']
    user_id = event['contact_id']
    print(incoming_message)
    if event['message']['direction'] == 'inbound' and redis.get(user_id):
        session_id = request.session_id
        chat_id = event['chat_id']
        get_gpt_answer.delay(incoming_message, session_id, chat_id)
    else:
        if incoming_message == 'Real person mode':
            redis.set(user_id, False)
        elif incoming_message == 'Bot mode':
            redis.set(user_id, True)
    return "Ok"
