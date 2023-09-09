import requests

from app.models import User
from config import env
from database import db_context

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    'X-Api-Key': env('RADIST_API_KEY'),
}


def send_answer(answer: str, chat_id: int):
    print('message from bot')
    url = f'https://api.radist.online/v2/companies/{env("COMPANY_ID")}/messaging/messages/'
    body = {
        "connection_id": env('CONNECTION_ID'),
        "chat_id": chat_id,
        "mode": "async",
        "message_type": "text",
        "text": {
            "text": f"{answer}"
        }
    }
    requests.post(url, headers=HEADERS, json=body)
