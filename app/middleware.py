from flask import request

from app.models import User
from app.utils import create_session_id
from database import db_context, redis


def middleware():
    event = request.json['event']
    user_id = event['contact_id']
    if event['message']['direction'] == 'inbound' and not redis.get(user_id):
        with db_context() as session:
            user = session.query(User).filter_by(id=user_id).one_or_none()
            if not user:
                user = User(id=user_id)
                redis.set(user_id, True)
                session_id = create_session_id(user)
                request.session_id = session_id
                user.conversation = session_id
                session.add(user)
            session.commit()

