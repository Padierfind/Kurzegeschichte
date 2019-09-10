print("In File: src/__init__.py")

import os
from flask import Flask

from bp.main_bp import main_bp
from bp.user_bp import user_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    app._static_folder = os.path.abspath("static/")
    return app