from flask import request, g

from database import redis
from .tasks import get_gpt_answer


def webhook():
    event = request.json['event']
    incoming_message = event['message']['text']['text']
    user_id = event['contact_id']
    print(incoming_message)
    if event['message']['direction'] == 'inbound' and bool(int(redis.get(user_id))):
        session_id = g.session_id
        chat_id = event['chat_id']
        get_gpt_answer.delay(incoming_message, session_id, chat_id)
    else:
        if incoming_message == 'Real person mode':
            print('Включился режим real person')
            redis.set(user_id, 0)
        elif incoming_message == 'Bot mode':
            print('Включился режим bot mode')
            redis.set(user_id, 1)
    return "Ok"
