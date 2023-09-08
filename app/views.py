from flask import request

from database import db_context
from . import app
from .gpt_utils import get_gpt_answer
from .models import User
from .radist_utils import send_answer


@app.route('/', methods=['POST'])
def webhook():
    event = request.json['event']
    incoming_message = event['message']['text']['text']
    user_id = event['contact_id']
    with db_context() as session:
        user = session.query(User).filter_by(id=user_id).one_or_none()
        if not user:
            user = User(id=user_id)
            session.add(user)
        gpt_answer = get_gpt_answer(incoming_message, user)
        send_answer(gpt_answer, user)
        session.commit()
    return gpt_answer
