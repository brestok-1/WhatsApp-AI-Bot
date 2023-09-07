import os

import requests

from app.models import User
from database import db_context


def get_gpt_answer(message: str, user_id) -> str:
    with db_context() as session:
        user = session.get(User, user_id)
        session_id = user.conversation
    if session_id:
        response = _get_gpt_response(message, session_id)
        answer = _parse_gpt_response(response)
    else:
        session_id = _create_session_id(user_id)
        response = _get_gpt_response(message, session_id)
        answer = _parse_gpt_response(response)
    return answer


def _get_gpt_response(message: str, session_id) -> dict:
    url = f"https://app.customgpt.ai/api/v1/projects/{os.getenv('GPT_MODEL')}/conversations/{session_id}/messages?stream=false&lang=en"
    payload = {
        'prompt': message
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'authorization': f'Bearer {os.getenv("API_KEY")}'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def _parse_gpt_response(response: dict) -> str:
    answer = response['data']['openai_response']
    answer = answer[:4000]
    return answer


def _create_session_id(user: User) -> str:
    with