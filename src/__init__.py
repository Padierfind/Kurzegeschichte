print("In File: src/__init__.py")

import os
from flask import Flask

from bp.main_bp import main_bp
from bp.user_bp import user_bp
from bp.authentication_bp import authentication_bp
from configs.flask_secret_key import secret


def create_app():
    print("In Method: create_app()")

    app = Flask(__name__)

    app.config.update(
        SECRET_KEY=secret
    )

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(authentication_bp)

    app._static_folder = os.path.abspath("static/")
    return app
