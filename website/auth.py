from flask import Blueprint, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .forms.LoginForm import LoginForm
from .forms.RegisterForm import RegisterForm
from data.users import User
from data import db_session


auth = Blueprint("auth", __name__, template_folder="../templates")


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('views.home'))
        return render_template("login.html", form=form, message="Неправильный логин или пароль")
    return render_template("login.html", form=form)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template("signup.html", title='Sign up', form=form)


@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))