print("In File: src/__init__.py")

import os
from bp.main_bp import main_bp
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app._static_folder = os.path.abspath("static/")
    return app