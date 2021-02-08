from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)


@auth.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullName = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password1')
        confirm = request.form.get('password2')

        if len(fullName) < 4:
            flash('Full Name must be greater than 4 characters', 'danger')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', 'danger')
        elif len(password) < 7 and password != confirm:
            flash("Password must be greater than 7 characters Or doesn't match", "danger")
        else:
            flash('Account Created...', 'success')

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "<h1> Logout Now </h1>"