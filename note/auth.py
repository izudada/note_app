from flask import Blueprint, render_template, request

auth = Blueprint("auth", __name__)


@auth.route('/register', methods=['GET', 'POST'])
def signup():
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "<h1> Logout Now </h1>"