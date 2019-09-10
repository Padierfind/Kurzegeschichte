print("In File: bp/user_bp.py")

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import os

template_dir = os.path.abspath('templates/')

user_bp = Blueprint('user_bps', __name__, template_folder=template_dir)

@user_bp.route('/editor')
def display_editor():
    print("In Method: display_editor()")

    try:
        return render_template('editor.html')
    except TemplateNotFound:
        abort(404)