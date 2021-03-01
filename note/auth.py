from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password1')
        confirm = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Sorry, this email is already a user')
        elif len(full_name) < 4:
            flash('Full Name must be greater than 4 characters', 'danger')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', 'danger')
        elif len(password) < 7 or password != confirm:
            flash("Password must be greater than 7 characters Or doesn't match", "danger")
        else:
            new_user = User(full_name=full_name, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('Account Created...', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully", "success")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('User does not exist', 'danger')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))