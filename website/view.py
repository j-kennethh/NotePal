from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .model import Note
from .import db

# Create view blueprint
view = Blueprint('view', __name__)


@view.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        note = request.form.get('note')

        # Ensure note is not empty
        if len(note) < 1:
            flash('Cannot add an empty note.', category='error')
            return redirect(url_for('view.index'))

        # Add the new note
        else:
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('view.index'))

    return render_template('index.html', user=current_user)


@view.route('/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def edit(id):

    note = Note.query.get(id)

    if request.method == 'POST':

        edited_note = request.form.get('note')

        # Edit the note if it exists
        if note:
            # Ensure the note belongs to the current user
            if note.user_id == current_user.id:
                note.text = edited_note
                db.session.commit()

        return redirect(url_for('view.index'))

    else:
        return render_template('edit.html', user=current_user, note=note)


@view.route('/<int:id>/delete/', methods=['GET'])
@login_required
def delete(id):

    note = Note.query.get(id)

    # Delete the note if it exists
    if note:
        # Ensure the note belongs to the current user
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return redirect(url_for('view.index'))
