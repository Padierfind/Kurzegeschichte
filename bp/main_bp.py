print("In File: bp/main_bp.py")

from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
import os

from src.db_handling import DbHandler

template_dir = os.path.abspath('templates/')

main_bp = Blueprint('main_bps', __name__, template_folder=template_dir)


@main_bp.route('/', methods=['GET'])
def display_main_index():
    print("In Method: display_main_index()")
    
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/story', methods=['GET'])
def display_story():
    print("In Method: display_story()")

    try:
        return render_template('story.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/get_story_data/<story_id>', methods=['GET'])
def ajax_get_story_data(story_id):
    print("In Method: ajax_get_story_data()")

    handler = DbHandler()
    db = 'test'  # Change when production
    collection = 'stories'
    result_of_db_operation = handler.read_one_doc_by_id_from_database(db_name=db, collection_name=collection,
                                                                      doc_id=story_id)

    if result_of_db_operation['success'] is True:
        return result_of_db_operation
    else:
        return 'NAY'
