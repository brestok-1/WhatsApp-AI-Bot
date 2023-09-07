from flask import Flask

from config import settings

app = Flask(__name__)
app.config.from_object(settings)

from . import views
