from flask import Flask, Blueprint
from config import settings


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(settings)

    from app.celery_app import create_celery
    app.celery_app = create_celery()

    views_bp = Blueprint('views', __name__)
    from .views import webhook
    views_bp.add_url_rule('/', view_func=webhook, methods=['POST'])
    app.register_blueprint(views_bp)

    from .middleware import middleware
    views_bp.before_request(middleware)

    return app


from . import views, models, tasks
