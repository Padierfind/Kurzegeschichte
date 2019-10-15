print("In File: bp/user_bp.py")

import os
from datetime import datetime
from flask import Blueprint, render_template, abort, request, url_for, redirect
from jinja2 import TemplateNotFound

from src.db_handling import DbHandler

template_dir = os.path.abspath('templates/')

user_bp = Blueprint('user_bps', __name__, template_folder=template_dir)


@user_bp.route('/editor', methods=['GET'])
def display_editor():
    print('In Method: display_editor()')

    try:
        return render_template('editor.html')
    except TemplateNotFound:
        abort(404)


@user_bp.route('/view_draft', methods=['GET'])
def view_draft():
    print('In Method: view_draft()')

    try:
        return render_template("story_preview.html")
    except TemplateNotFound:
        abort(404)


@user_bp.route('/save_draft', methods=['POST'])
def save_draft_and_redirect():
    print('In Method: save_draft_and_redirect()')

    title: str = request.form.get('title')
    content: str = request.form.get('content')
    timestamp: datetime = datetime.now()
    user_id: int = 1

    test_dict = {
        'title': title,
        'content': content,
        'timestamp': timestamp,
        'user_id': user_id,
        'reading_time': round(len(content) / 1500),
        'public': False,
        'public_with_link': False
    }

    handler = DbHandler()
    db = "test" # Change when production
    collection = "stories"
    result_of_db_operation = handler.write_to_database(db_name=db, collection_name=collection, json_to_write=test_dict)

    if result_of_db_operation['success'] is True:
        return redirect(url_for('user_bps.view_draft', story_id=result_of_db_operation['doc_id']))
    else:
        return redirect(url_for('user_bps.display_editor', notification='Etwas ist schief gelaufen. Bitte versuche es '
                                                                        'später noch ein Mal.'))


@user_bp.route('/publish_story', methods=['POST'])
def publish_story_and_redirect():
    print('In Method: publish_story_and_redirect()')

    story_id: str = request.form.get('story_id')
    title: str = request.form.get('title')
    user_id: str = request.form.get('user_id')
    reading_time: str = request.form.get('reading_time')
    preview_text: str = request.form.get('preview_text')
    categories: str = request.form.getlist('selected_categories')
    timestamp: datetime = request.form.get('timestamp')

    test_dict = {
        'story_id': story_id,
        'title': title,
        'preview_text': preview_text,
        'timestamp': timestamp,
        'user_id': user_id,
        'story_id': story_id,
        'reading_time': reading_time,
        'categories': categories
    }

    handler = DbHandler()
    db = "test"  # Change when production
    collection = "previews"
    result_of_db_operation = handler.write_to_database(db_name=db, collection_name=collection, json_to_write=test_dict)

    if result_of_db_operation['success'] is True:
        return redirect(url_for('main_bps.display_story', story_id=story_id))
    else:
        return redirect(url_for('user_bps.display_editor', notification='Etwas ist schief gelaufen. Bitte versuche es '
                                                                        'später noch ein Mal.'))
