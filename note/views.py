from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import Category, Note
from . import db
import json

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

            flash("Category created", "success") 
            return redirect(url_for('views.home'))

    categories = Category.query.filter_by(user_id=user_id).all()
    if categories:
        return render_template("user/dashboard.html", user=current_user, categories=categories)
    else:
        flash("You have not created a category yet", "success")
        return render_template("user/dashboard.html", user=current_user)

@views.route('/categories/<int:cat_id>/notes', methods=['GET', 'POST'])
@login_required
def view_category(cat_id):
    user_id = current_user.get_id()
    notes = Note.query.filter_by(category_id=cat_id).all()
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        if len(body) < 1 or len(title) < 1:
            flash("Sorry, Title and Body can't be empty", "danger") 
            return redirect(url_for('views.view_category'))
        else:
            new_note = Note(title=title, body=body, user_id=user_id, category_id=cat_id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note has been added", "success")
            return redirect(url_for('views.view_category', cat_id=cat_id)) 

    if len(notes) < 1:
        flash("You have no notes for this category", "success")
        return render_template('user/category.html')
    else:
        return render_template('user/category.html', notes=notes)

@views.route('/categories/<int:cat_id>/notes/<int:note_id>', methods=['GET', 'POST'])
@login_required
def view_notes(cat_id, note_id):
    user_id = current_user.get_id()
    note = Note.query.filter_by(id=note_id).one()

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        if len(body) < 1 or len(title) < 1:
            flash("Sorry, Title and Body can't be empty", "danger") 
            return request.url
        else:
            note.title = title
            note.body = body
            db.session.commit()
            flash("Note has been updated", "success")
            return redirect(url_for('views.view_notes', note_id=note_id))

    if not note:
        flash("Note no longer exist", "danger")
        return render_template('user/note.html')
    else:
        return render_template('user/note.html', note=note, note_id=note_id)

@views.route('/delete_category', methods=['POST'])
@login_required
def delete_category():
    category = json.loads(request.data)
    category_id = category['catID']
    category = Category.query.get(category_id)
    if category:
        if category.user_id == current_user.id:
            notes = Note.query.filter_by(category_id=category_id).all()
            if notes:
                for note in notes:
                    db.session.delete(note)
                    db.session.commit()
                
            db.session.delete(category)
            db.session.commit()

            flash("Category Deleted", "success")
        
    return jsonify({})