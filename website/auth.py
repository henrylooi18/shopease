from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import UserDatabase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = UserDatabase.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You have logged in.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('routes.home'))
            else:
                flash('Password incorrect, please try again.', category='error')
        else:
            flash('Your email is not registered in the server.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout/')
@login_required  # have to be logged in to log out
def logout():
    logout_user()
    flash('You have logged out.', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password = request.form.get('password')

        user = UserDatabase.query.filter_by(email=email).first()

        if user:
            flash('Your account already exists in the server.', category='error')
        elif len(password) < 8:
            flash('Your password needs to have a minimum of 8 characters.', category='error')
        else:
            new_user = UserDatabase(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash('Your account has been successfully registered!', category='success')
            return redirect(url_for('routes.home'))

    return render_template("register.html", user=current_user)


@auth.route("/profile/", methods=['GET', 'POST'])
@login_required
def profile():
    userDetails = UserDatabase.query.filter_by(id=current_user.id).first()

    return render_template('profile.html', userDetails=userDetails, user=current_user)
