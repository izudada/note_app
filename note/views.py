from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Category
from . import db

views = Blueprint("views", __name__)

@views.route('/')
def index():
    return render_template("index.html", user=current_user)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        if len(title) < 1:
            flash("Sorry, Titlecan't be empty", "danger") 
            return redirect(url_for('views.home'))
        else:
            new_category = Category(title=title)
            db.session.add(new_category)
            db.session.commit()

            flash("Category created", "danger") 
            return redirect(url_for('views.home'))

    user_id = current_user.get_id()
    categories = Category.query.filter_by(id=user_id).all()
    if categories:
        return render_template("dashboard.html", user=current_user, categories=categories)
    else:
        flash("You have not created a category yet", "success")
        return render_template("dashboard.html", user=current_user)

# @views.route('/category', methods=['POST'])
# def add_category():
#     pass

@views.route('/categories/add_note', methods=['POST'])
def add_note():
    title = request.form.get('title')
    body = request.form.get('body')

    if len(body) < 1 or len(title) < 1:
        flash("Sorry, Title and Body can't be empty", "danger") 
        return redirect(url_for('home'))
    else:
        new_note = Note()
        flash("Note has been added", "success")
        return redirect(url_for('home')) 
