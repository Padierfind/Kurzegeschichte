print("In File: bp/main_bp.py")

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import os

from src.db_handling import db_handler

template_dir = os.path.abspath('templates/')

main_bp = Blueprint('main_bps', __name__, template_folder=template_dir)

@main_bp.route('/')
def display_main_index():
    print("In Method: display_main_index()")
    
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@main_bp.route('/story')
def display_story():
    print("In Method: display_story()")

    try:
        return render_template('story.html')
    except TemplateNotFound:
        abort(404)

@main_bp.route('/test')
def test():
    print("In Method: test()")

    handler = db_handler()

    test_dict = {
        "Hallo" : "asbdqweoiwqe",
        "Ich heiße" : "Patrick"
    }

    db = "tests"
    collection = "unit_tests"
    handler.write_to_database(db_name=db, collection_name=collection, json_to_write=test_dict)