from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Create authentication blueprint
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # Retrieve data from the form
        email = request.form.get('email')
        password = request.form.get('password')

        # Ensure user has an account registered
        user = User.query.filter_by(email=email).first()

        # Ensure password matches
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('view.index'))
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Email does not exist.', category='error')
            return redirect(url_for('auth.login'))

    else:
        return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # Retrieve data from the form
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        user = User.query.filter_by(email=email).first()

        # Ensure email was submitted
        if not email:
            flash('Must provide an email.', category='error')
            return redirect(url_for('auth.register'))

        # Ensure email does not already exist
        elif user:
            flash('Email already exists.', category='error')
            return redirect(url_for('auth.register'))

        # Ensure name was submitted
        elif not name:
            flash('Must provide a name.', category='error')
            return redirect(url_for('auth.register'))

        # Ensure name is not more than 16 characters
        elif len(name) > 16:
            flash('Name must be at most 16 characters in length.', category='error')
            return redirect(url_for('auth.register'))

        # Ensure password was submitted
        elif not password:
            flash('Must provide a password.', category='error')
            return redirect(url_for('auth.register'))

        # Ensure confirmation was submitted
        elif not confirmation:
            flash('Must provide confirmation of password.', category='error')
            return redirect(url_for('auth.register'))

        # Ensure passowrd is at least 6 characters in length
        elif len(password) < 6:
            flash('Password must be at least 6 characters in length.', category='error')
            return redirect(url_for('auth.register'))

        # Ensure password and confirmation match
        elif password != confirmation:
            flash('Passwords do not match.', category='error')
            return redirect(url_for('auth.register'))

        # Register the user
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Account Registered!', category='success')
            return redirect(url_for('view.index'))

    else:
        return render_template('register.html', user=current_user)
