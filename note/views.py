from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Category, Note
from . import db

views = Blueprint("views", __name__)

@views.route('/')
def index():
    return render_template("index.html", user=current_user)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    user_id = current_user.get_id()
    if request.method == 'POST':
        title = request.form.get('title')
        if len(title) < 1:
            flash("Sorry, Titlecan't be empty", "danger") 
            return redirect(url_for('views.home'))
        else:
            new_category = Category(title=title, user_id=user_id)
            db.session.add(new_category)
            db.session.commit()

            flash("Category created", "danger") 
            return redirect(url_for('views.home'))

    categories = Category.query.filter_by(user_id=user_id).all()
    if categories:
        return render_template("dashboard.html", user=current_user, categories=categories)
    else:
        flash("You have not created a category yet", "success")
        return render_template("dashboard.html", user=current_user)

@views.route('/categories/<int:cat_id>/notes')
@login_required
def view_category(cat_id):
    notes = Note.query.filter_by(category_id=cat_id).all()
    if len(notes) < 1:
        flash("You have no notes for this category", "success")
        return render_template('category.html')
    else:
        return render_template('category.html', notes=notes)

@views.route('/categories/add_note', methods=['POST'])
@login_required
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
