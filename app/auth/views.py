from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from ..models import User
from .forms import RegistrationForm, LoginForm
from ..email import mail_message


@auth.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid email or password')

    title = "Login to Reilly's Blog"
    return render_template('auth/login.html', form = form, title = title)


@auth.route('/register', methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        User.save_user(user)
        mail_message("Welcome to Reilly's Blog", "email/welcome", user.email, user=user)
        return redirect(url_for('auth.login'))

    title = 'New account'
    return render_template('auth/register.html', form = form, title = title)

@auth.route('/logout')
@login_required
def logout():
    logout_user( )
    return redirect(url_for('main.index'))