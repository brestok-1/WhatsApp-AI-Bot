from celery import shared_task

from app.models import User
from app.utils import get_gpt_response, parse_gpt_response, create_session_id, send_answer
from database import db_context


@shared_task
def get_gpt_answer(message: str, user_id: int, chat_id: int) -> str:
    with db_context() as session:
        print('Запуск')
        user = session.query(User).filter_by(id=user_id).one_or_none()
        if not user:
            user = User(id=user_id)
            session.add(user)
        session_id = user.conversation
        if session_id:
            response = get_gpt_response(message, session_id)
            answer = parse_gpt_response(response)
        else:
            session_id = create_session_id(user)
            user.conversation = session_id
            session.add(user)
            response = get_gpt_response(message, session_id)
            answer = parse_gpt_response(response)
            session.commit()
    send_answer(answer=answer, chat_id=chat_id)
    return answer
