from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .forms.LoginForm import LoginForm
from .forms.RegisterForm import RegisterForm
from data.users import User
from data import db_session


auth = Blueprint("auth", __name__, template_folder="../templates")


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        abort(404)
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Logged in!", category="success")
            return redirect(url_for('views.home'))
        flash("Неправильный логин или пароль.", category="danger")
    return render_template("login.html", title='Login', form=form, user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if not current_user.is_anonymous:
        abort(404)
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash("Пароли не совпадают!", "warning")
            return render_template("signup.html", title='Sign up', form=form, user=current_user)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash("Такой пользователь уже есть!", "warning")
            return render_template("signup.html", title='Sign up', form=form, user=current_user)
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        flash("Вы зарегистрированы!", "success")
        return redirect(url_for('auth.login'))
    return render_template("signup.html", title='Sign up', form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта")
    return redirect("/")