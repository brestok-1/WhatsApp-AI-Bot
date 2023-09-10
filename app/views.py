from flask import request
from .tasks import get_gpt_answer


def webhook():
    event = request.json['event']
    incoming_message = event['message']['text']['text']
    print(incoming_message)
    if event['message']['direction'] == 'inbound':
        user_id = event['contact_id']
        chat_id = event['chat_id']
        print('Отправил человек!!!!')
        get_gpt_answer.delay(incoming_message, user_id, chat_id)
    else:
        print('Отправил бот!!!')
    return "Ok"
