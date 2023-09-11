import requests

from app.models import User
from config import env

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    'X-Api-Key': env('RADIST_API_KEY'),
}


def send_answer(answer: str, chat_id: int):
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


def get_gpt_response(message: str, session_id : int) -> dict:
    url = f"https://app.customgpt.ai/api/v1/projects/{env('GPT_MODEL')}/conversations/{session_id}/messages?stream=false&lang=en"
    payload = {
        'prompt': message
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'authorization': f'Bearer {env("GPT_API_KEY")}'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def parse_gpt_response(response: dict) -> str:
    answer = response['data']['openai_response']
    answer = answer[:4000]
    return answer


def create_session_id(user: User) -> str:
    url = f"https://app.customgpt.ai/api/v1/projects/{env('GPT_MODEL')}/conversations"

    payload = {"name": str(user.id)}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {env('GPT_API_KEY')}"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    session_id = response.json()['data']['session_id']
    return session_id
