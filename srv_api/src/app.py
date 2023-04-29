import click
from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config.settings import Settings
from services.user_service import UserService
from api import api_blueprint

SETTINGS = Settings()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'changeme'

app.register_blueprint(api_blueprint)

limiter = Limiter(
    app, key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour", "1 per minute"],
    storage_uri=SETTINGS.REDIS_URL,
    # storage_options={"connect_timeout": 30},
    strategy="fixed-window",  # or "moving-window"
)


@app.route('/')
def get_docs():
    return render_template('swaggerui.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8005,
        debug=True
    )
