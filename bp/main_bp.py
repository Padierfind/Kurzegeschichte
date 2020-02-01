print("In File: bp/main_bp.py")

from flask import Blueprint, render_template, abort, request, session, redirect, url_for, send_file
from jinja2 import TemplateNotFound
import os

from src.db_handling import DbHandler

template_dir = os.path.abspath('templates/')

main_bp = Blueprint('main_bps', __name__, template_folder=template_dir)


@main_bp.route('/', methods=['GET'])
def display_main_index():
    print('In Method: display_main_index()')
    
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/story', methods=['GET'])
def display_story():
    print('In Method: display_story()')

    try:
        return render_template('story.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/imprint', methods=['GET'])
def display_imprint():
    print('In Method: display_imprint()')

    try:
        return render_template('imprint.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/privacy', methods=['GET'])
def display_privacy():
    print('In Method: display_privacy()')

    try:
        return render_template('privacy.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/terms', methods=['GET'])
def display_terms():
    print('In Method: display_terms()')

    try:
        return render_template('terms.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/info', methods=['GET'])
def display_info():
    print('In Method: display_info()')

    try:
        return render_template('info.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/press', methods=['GET'])
def display_press():
    print('In Method: display_press()')

    try:
        return redirect(url_for('static', filename='files/presskit_de.pdf'))
    except TemplateNotFound:
        abort(404)


@main_bp.route('/profile', methods=['GET'])
def display_profile():
    print('In Method: display_profile()')

    user_id = request.args.get('user')

    if user_id == 'user':
        try:
            current_user_id = session['user_id']
            return redirect(url_for('main_bps.display_profile', user=current_user_id))
        except Exception as e:
            print('Not logged in.')
            print(e)

    try:
        return render_template('profile.html')
    except TemplateNotFound:
        abort(404)


@main_bp.route('/get_story_data/<story_id>', methods=['GET'])
def async_get_story_data(story_id):
    print('In Method: async_get_story_data()')

    handler = DbHandler()
    db = 'production'
    collection = 'stories'
    result_of_db_operation_story = handler.read_one_doc_by_id_from_database(db_name=db, collection_name=collection,
                                                                            doc_id=story_id)

    collection = 'previews'
    param_name = 'story_id'
    result_of_db_operation_preview = handler.read_one_doc_by_param_from_database(db_name=db, collection_name=collection,
                                                                                 doc_value=story_id,
                                                                                 doc_param=param_name)

    if result_of_db_operation_story['success'] is True & result_of_db_operation_preview['success'] is True:

        result = result_of_db_operation_preview['result']
        result.update(result_of_db_operation_story['result'])

        return result
    else:
        return 'False'


@main_bp.route('/get_story_previews/', methods=['GET'])
def async_get_story_previews():
    print('In Method: async_get_story_previews()')

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
    db = 'production'
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
    print('In Method: async_get_user_story_previews()')

    handler = DbHandler()
    db = 'production'
    collection = 'previews'

    param_name = 'user_id'

    result_of_db_operation = handler.read_multiple_docs_by_param_from_database(db_name=db, collection_name=collection,
                                                                               doc_value=user_id, doc_param=param_name)

    if result_of_db_operation['success'] is True:
        return result_of_db_operation
    else:
        return 'False'


@main_bp.route('/get_login_status', methods=['GET'])
def async_get_login_status():
    print('In Method: async_get_login_status()')

    try:
        current_user_id = session['user_id']

        result_dict = {
            'logged_in': True,
            'user_name': current_user_id
        }

        return result_dict
    except Exception as e:
        print('Not logged in.')

        return 'False'


@main_bp.route('/get_comments/<story_id>', methods=['GET'])
def async_get_comments(story_id):
    print('In Method: async_get_comments()')

    handler = DbHandler()
    db = 'production'
    collection = 'comments'

    param_name = 'story_id'

    result_of_db_operation = handler.read_multiple_docs_by_param_from_database(db_name=db, collection_name=collection,
                                                                               doc_value=story_id, doc_param=param_name)

    if result_of_db_operation['success'] is True:
        return result_of_db_operation
    else:
        return 'False'
