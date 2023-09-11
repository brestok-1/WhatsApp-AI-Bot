from flask import request, g

from app.models import User
from app.utils import create_session_id
from database import db_context, redis


def middleware():
    event = request.json['event']
    user_id = event['contact_id']
    res = redis.get(name=f'is_user_exist:{user_id}')
    if event['message']['direction'] == 'inbound':
        with db_context() as session:
            if not res:
                user = User(id=user_id)
                redis.set(user_id, 1)
                redis.set(f'is_user_exist:{user_id}', 1)
                session_id = create_session_id(user)
                user.conversation = session_id
                g.session_id = session_id
                session.add(user)
                session.commit()
            else:
                user = session.get(User, user_id)
                g.session_id = user.conversation
