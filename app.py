print("In File: app.py")

from flask_login import LoginManager
from src import create_app
from src.authentication import User
from flask import redirect, url_for
app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    print("In Method: load_user()")

    return User(user_id=user_id)


@login_manager.unauthorized_handler
def handle_unauthorized_access():
    print("In Method: handle_unauthorized_access()")

    return redirect(url_for('authentication_bps.display_login_registration_page', notification='Bitte logge dich ein,'
                                                                                               'um diese Seite zu'
                                                                                               'besuchen.'))


if __name__ == "__main__":
    print("Is __main__")

    try:
        app.run(host='127.0.0.1', port=5000)
    except OSError as e:
        print(e)
