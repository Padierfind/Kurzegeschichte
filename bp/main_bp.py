print("In File: bp/main_bp.py")

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import os

template_dir = os.path.abspath('templates/')

main_bp = Blueprint('main_bps', __name__, template_folder=template_dir)
print(template_dir)

@main_bp.route('/')
def show_main_index():
    print("In Method: show_main_index()")
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)