from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a2346.@'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefic='/')
    app.register_blueprint(auth, url_prefic='/')

    return app