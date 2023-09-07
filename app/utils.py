import os

import requests


def get_gpt_answer(message: str) -> str:
    url = "https://app.customgpt.ai/api/v1/projects/projectId/conversations/sessionId/messages?stream=false&lang=en"
    payload = {
        'prompt': message
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'authorization': f'Bearer {os.getenv("API_KEY")}'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text
