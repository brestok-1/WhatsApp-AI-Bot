import os

import requests

from app.models import User
from config import env
from database import db_context


def get_gpt_answer(message: str, user: User) -> str:
    with db_context() as session:
        session_id = user.conversation
        if session_id:
            response = _get_gpt_response(message, session_id)
            answer = _parse_gpt_response(response)
        else:
            session_id = _create_session_id(user)
            user.conversation = session_id
            session.add(user)
            response = _get_gpt_response(message, session_id)
            answer = _parse_gpt_response(response)
    return answer


def _get_gpt_response(message: str, session_id) -> dict:
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


def _parse_gpt_response(response: dict) -> str:
    answer = response['data']['openai_response']
    answer = answer[:4000]
    return answer


def _create_session_id(user: User) -> str:
    url = f"https://app.customgpt.ai/api/v1/projects/{env('GPT_MODEL')}/conversations"

    payload = {"name": user.id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {env('GPT_API_KEY')}"
    }

    response = requests.post(url, json=payload, headers=headers)
    session_id = response.json()['data']['session_id']
    return session_id
