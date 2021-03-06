print("In File: bp/authentication_bp.py")

import os
from flask import Blueprint, render_template, abort, request, redirect, url_for, session
from jinja2 import TemplateNotFound
from flask_login import login_user, login_required, logout_user

from src.authentication import User
from src.db_handling import DbHandler
from src.mail_handling import mail_handling

template_dir = os.path.abspath('templates/')

authentication_bp = Blueprint('authentication_bps', __name__, template_folder=template_dir)


@authentication_bp.route('/login', methods=['GET'])
def display_login_registration_page():
    print("In Method: display_login_registration_page()")

    try:
        return render_template('login.html')
    except TemplateNotFound:
        abort(404)


@authentication_bp.route('/register_user', methods=['POST'])
def register_user():
    print("In Method: register_user()")

    user_id: str = request.form.get('name')
    email: str = request.form.get('email')
    password: str = request.form.get('password')

    new_user = User(user_id=user_id, email=email, password=password)
    user_signed_up = False

    try:
        user_signed_up = new_user.sign_up()
    except Exception as e:
        print(e)

    try:
        confirmation_mail_sent = mail_handling.send_confirmation_mail(name=user_id, email=email)
    except Exception as e:
        print(e)

    if (user_signed_up == True) and (confirmation_mail_sent == True):
        return redirect(url_for('main_bps.display_main_index', notification='Herzlich Willkommen! Bitte schau in '
                                                                            'deinem Email Postfach nach und bestätige '
                                                                            'deine Registrierung.'))
    else:
        return redirect(url_for('authentication_bps.display_login_registration_page', notification='Etwas ist bei deiner'
                                                                                                   ' Registrierung '
                                                                                                   'fehlgeschlagen. '
                                                                                                   'Das Tut uns leid. '
                                                                                                   'Bitte versuche es '
                                                                                                   'erneut.'))


@authentication_bp.route('/login_user', methods=['POST'])
def verify_and_login_user():
    print("In Method: verify_and_login_user()")

    email: str = request.form.get('email')
    password: str = request.form.get('password')

    user = User(email=email, password=password)
    user_from_db = user.check_if_user_exists()

    if not user_from_db:
        return redirect(url_for('authentication_bps.display_login_registration_page', notification='Bitte registriere '
                                                                                                   'dich zuerst.'))
                                                                                                   
    user_id: str = user_from_db['result']['user_id']

    is_authenticated = user.check_password(saved_password=user_from_db['result']['password'], input_password=password)

    if is_authenticated:
        print("User is authenticated. Login now.")
        login_user(user)
        session['user_id'] = user_id

        return redirect(url_for('main_bps.display_main_index', notification='Willkommen zurück, ' + user_id + '!'))
    else:
        print("User is NOT authenticated.")

        return redirect(url_for('authentication_bps.display_login_registration_page', notification='Etwas stimmt mit '
                                                                                                   'deinem Passwort'
                                                                                                   ' nicht. Bitte '
                                                                                                   'probiere es '
                                                                                                   'erneut.'))


@authentication_bp.route('/confirm_registration', methods=['GET'])
def confirm_mail():
    print("In Method: confirm_mail()")

    user_id = request.args.get('user_id')

    handler = DbHandler()
    db = 'test' # change for production
    collection = 'users'

    param_name_find = 'user_id'

    param_name_new = 'mail_confirmed'
    result_of_db_operation = handler.update_one_doc_by_param_from_database(db_name=db, collection_name=collection,
                                                                                 doc_value_find=user_id,
                                                                                 doc_param_find=param_name_find,
                                                                                 doc_value_new=True,
                                                                                 doc_param_new=param_name_new)

    if result_of_db_operation['success'] is True:
        return redirect(url_for('main_bps.display_main_index', notification='Dein Profil ist jetzt bestätigt.'))
    else:
        return redirect(url_for('main_bps.display_main_index', notification='Etwas ist schief gelaufen. Bitte versuche es '
                                                                        'später noch ein Mal.'))


@authentication_bp.route('/delete_account', methods=['GET'])
@login_required
def delete_account():
    print('In Method: delete_account()')
    handler = DbHandler()
    db = 'test' # change for production
    result_of_db_operation = handler.delete_from_all_collections_by_user_id(db_name=db, user_id=session['user_id'])

    if result_of_db_operation['success'] is True:
        logout_user()
        return redirect(url_for('main_bps.display_main_index', notification='Schade, dass du uns verlassen hast. Es ist'
                                                                            'nie zu spät zurück zu kommen!'))
    else:
        return redirect(url_for('user_bps.display_settings', notification='Etwas ist schief gelaufen. Bitte versuche es'
                                                                          ' später noch ein Mal.'))


@authentication_bp.route("/logout")
@login_required
def logout_user_endpoint():
    print("In Method: logout_user_endpoint()")

    logout_user()
    return redirect(url_for('main_bps.display_main_index', notification='Du wurdest ausgeloggt. ''Wir freuen uns auf '
                                                                                               'deinen nächsten '
                                                                                               'Besuch.'))
