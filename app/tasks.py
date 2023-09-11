from celery import shared_task

from app.utils import get_gpt_response, parse_gpt_response, create_session_id, send_answer


@shared_task
def get_gpt_answer(message: str, session_id: int, chat_id: int) -> str:
    print('gpt work')
    response = get_gpt_response(message, session_id)
    answer = parse_gpt_response(response)
    send_answer(answer=answer, chat_id=chat_id)
    return answer
