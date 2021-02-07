from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route('/register')
def signup():
    return "<h1> Sign Up</h1>"

@auth.route('/login')
def login():
    return "<h1> Login Here</h1>"

@auth.route('/logout')
def logout():
    return "<h1> Logout Now </h1>"