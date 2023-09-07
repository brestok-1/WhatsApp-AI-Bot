import os

import requests


def get_gpt_answer(message: str) -> str:
    response = _get_gpt_response(message)
    answer = _parse_gpt_response(response)
    return answer


def _get_gpt_response(message: str) -> dict:
    url = "https://app.customgpt.ai/api/v1/projects/7364/conversations/68fb1009-e415-47fe-90f0-637862b966dc/messages?stream=false&lang=en"
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
