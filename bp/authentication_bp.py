print("In File: bp/authentication_bp.py")

import os
from flask import Blueprint, render_template, abort, request, redirect, url_for
from jinja2 import TemplateNotFound
from flask_login import login_user, login_required, logout_user

from src.authentication import User

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

    name: str = request.form.get('name')
    email: str = request.form.get('email')
    password: str = request.form.get('password')

    new_user = User(name=name, email=email, password=password)
    signup = False

    try:
        signup = new_user.sign_up()
    except Exception as e:
        print("Something went wrong:")
        print(e)

    if signup == True:
        return redirect(url_for('authentication_bps.display_login_registration_page', notification='Herzlich '
                                                                                                   'Willkommen!'
                                                                                                   ' Bitte schau in '
                                                                                                   'deinem Email '
                                                                                                   'Postfach nach und '
                                                                                                   'bestätige deine '
                                                                                                   'Registrierung.'))
    else:
        # TODO ERROR MESSAGE
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

    is_authenticated = user.check_password(saved_password=user_from_db['result']['password'], input_password=password)

    if is_authenticated:
        login_user(user)
        return redirect(url_for('main_bps.display_main_index', notification='Willkommen zurück!'))
    else:
        return redirect(url_for('authentication_bps.display_login_registration_page', notification='Etwas stimmt mit '
                                                                                                   'deinem Passwort'
                                                                                                   ' nicht. Bitte '
                                                                                                   'probiere es '
                                                                                                   'erneut.'))


@authentication_bp.route("/logout")
@login_required
def logout_user():
    print("In Method: logout_user()")

    logout_user()
    return redirect(url_for('authentication_bps.display_login_registration_page', notification='Du wurdest ausgeloggt. '
                                                                                               'Wir freuen uns auf '
                                                                                               'deinen nächsten '
                                                                                               'Besuch.'))