from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KAY'] = 'a2346.@'

    return app