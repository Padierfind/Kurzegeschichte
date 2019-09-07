print("In File: app.py")

from flask import Flask
from src import create_app

app = create_app()

if __name__ == "__main__":
    print("Is __main__")

    try:
        app.run(host='0.0.0.0', port=80)
    except OSError as e:
        print(e)