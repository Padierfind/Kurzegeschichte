print("In File: bp/user_bp.py")

import os
from math import ceil
from datetime import datetime
from flask import Blueprint, render_template, abort, request, url_for, redirect, session
from jinja2 import TemplateNotFound
from flask_login import login_required

from src.db_handling import DbHandler

template_dir = os.path.abspath('templates/')

user_bp = Blueprint('user_bps', __name__, template_folder=template_dir)


@user_bp.route('/editor', methods=['GET'])
@login_required
def display_editor():
    print('In Method: display_editor()')

    try:
        return render_template('editor.html')
    except TemplateNotFound:
        abort(404)


@user_bp.route('/settings', methods=['GET'])
@login_required
def display_settings():
    print('In Method: display_settings()')

    try:
        return render_template('settings.html')
    except TemplateNotFound:
        abort(404)


@user_bp.route('/view_draft', methods=['GET'])
@login_required
def view_draft():
    print('In Method: view_draft()')

    try:
        return render_template("story_preview.html")
    except TemplateNotFound:
        abort(404)


@user_bp.route('/save_draft', methods=['POST'])
@login_required
def save_draft_and_redirect():
    print('In Method: save_draft_and_redirect()')

    title: str = request.form.get('title')
    content: str = request.form.get('content')
    timestamp: datetime = datetime.now()
    user_id: str = session['user_id']
    reading_time: int = ceil(len(content) / 1500);

    test_dict = {
        'title': title,
        'content': content,
        'timestamp': timestamp,
        'user_id': user_id,
        'reading_time': reading_time,
        'public': True,
        'public_with_link': True
    }

    handler = DbHandler()
    db = 'test' # change for production
    collection = "stories"
    result_of_db_operation = handler.write_to_database(db_name=db, collection_name=collection, json_to_write=test_dict)

    if result_of_db_operation['success'] is True:
        return redirect(url_for('user_bps.view_draft', story_id=result_of_db_operation['doc_id']))
    else:
        return redirect(url_for('user_bps.display_editor', notification='Etwas ist schief gelaufen. Bitte versuche es '
                                                                        'später noch ein Mal.'))


@user_bp.route('/publish_story', methods=['POST'])
@login_required
def publish_story_and_redirect():
    print('In Method: publish_story_and_redirect()')

    story_id: str = request.form.get('story_id')
    title: str = request.form.get('title')
    user_id: str = request.form.get('user_id')
    reading_time: int = int(request.form.get('reading_time'))
    preview_text: str = request.form.get('preview_text')
    categories: str = request.form.getlist('selected_categories')
    timestamp: datetime = request.form.get('timestamp')
    length: str = 'veryshort'

    if reading_time >= 5:
        length = 'short'
        if reading_time > 15:
            length = 'medium'
            if reading_time > 45:
                length = 'long'

    test_dict = {
        'story_id': story_id,
        'title': title,
        'preview_text': preview_text,
        'timestamp': timestamp,
        'user_id': user_id,
        'story_id': story_id,
        'reading_time': reading_time,
        'categories': categories,
        'length': length,
        'classic': False
    }

    handler = DbHandler()
    db = 'test' # change for production
    collection = "previews"
    result_of_db_operation = handler.write_to_database(db_name=db, collection_name=collection, json_to_write=test_dict)

    if result_of_db_operation['success'] is True:
        return redirect(url_for('main_bps.display_story', story_id=story_id, notification='Herzlichen Glückwunsch! Deine Story wurde soeben veröffentlicht.'))
    else:
        return redirect(url_for('user_bps.display_editor', notification='Etwas ist schief gelaufen. Bitte versuche es '
                                                                        'später noch ein Mal.'))



@user_bp.route('/get_story_data_without_preview/<story_id>', methods=['GET'])
@login_required
def async_get_story_data_without_preview(story_id):
    print('In Method: get_story_data_without_preview()')

    handler = DbHandler()
    db = 'test' # change for production
    collection = 'stories'
    result_of_db_operation_story = handler.read_one_doc_by_id_from_database(db_name=db, collection_name=collection,
                                                                            doc_id=story_id)

    if result_of_db_operation_story['success'] is True:
        return result_of_db_operation_story
    else:
        return 'False'


@user_bp.route('/publish_comment', methods=['POST'])
@login_required
def publish_comment():
    print('In Method: publish_comment()')

    content: str = request.form.get('content')
    timestamp: datetime = datetime.now()
    user_id: str = session['user_id']
    story_id: str = request.form.get('story_id')

    test_dict = {
        'content': content,
        'timestamp': timestamp,
        'user_id': user_id,
        'story_id': story_id
    }

    handler = DbHandler()
    db = 'test' # change for production
    collection = "comments"
    result_of_db_operation = handler.write_to_database(db_name=db, collection_name=collection,
                                                       json_to_write=test_dict)

    if result_of_db_operation['success'] is True:
        return redirect(url_for('main_bps.display_story', story_id=story_id, notification='Dein Kommentar wurde '
                                                                                          'veröffentlicht. Danke dafür,'
                                                                                          ' dass du ein Teil dieser '
                                                                                          'Community bist!'))
    else:
        return redirect(url_for('main_bps.display_story', story_id=story_id, notification='Etwas ist schief gelaufen. '
                                                                                          'Bitte versuche es '
                                                                                          'später noch ein Mal.'))
