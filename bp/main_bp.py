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


@main_bp.route('/profile', methods=['GET'])
def display_profile():
    print("In Method: display_profile()")

    try:
        return render_template('profile.html')
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
        return 'False'


@main_bp.route('/get_story_previews/', methods=['GET'])
def async_get_story_previews():
    print("In Method: async_get_story_previews()")

    index = request.args.get('index')

    selected_categories = []
    selected_lengths = []

    try:
        categories_in_url = request.args.get('categories')
        selected_categories = categories_in_url.split(',')
    except Exception as e:
        print("No categories in Url specified.")

    try:
        lengths_in_url = request.args.get('lengths')
        selected_lengths = lengths_in_url.split(',')
    except Exception as e:
        print("No lengths in Url specified.")

    handler = DbHandler()
    db = 'test'  # Change when production
    collection = 'previews'
    result_of_db_operation = handler.read_document_previews(db_name=db, collection_name=collection,
                                                            starting_id=int(index), amount_of_documents=8,
                                                            categories=selected_categories, lengths=selected_lengths)

    if result_of_db_operation['success'] is True:
        return result_of_db_operation
    else:
        return 'False'


@main_bp.route('/get_user_story_previews/<user_id>', methods=['GET'])
def async_get_user_story_previews(user_id):
    print("In Method: async_get_user_story_previews()")

    handler = DbHandler()
    db = 'test'  # Change when production
    collection = 'previews'

    param_name = 'user_id'

    result_of_db_operation = handler.read_multiple_docs_by_param_from_database(db_name=db, collection_name=collection,
                                                                               doc_value=user_id, doc_param=param_name)

    if result_of_db_operation['success'] is True:
        return result_of_db_operation
    else:
        return 'False'