print("In File: app.py")

from flask_login import LoginManager
from src import create_app
from src.authentication import User

app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    print("In Method: load_user()")

    return User(user_id=user_id)


if __name__ == "__main__":
    print("Is __main__")

    try:
        app.run(host='127.0.0.1', port=5000)
    except OSError as e:
        print(e)
