from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask_login import login_user, login_required, logout_user, current_user
from .forms.LoginForm import LoginForm
from .forms.RegisterForm import RegisterForm
from .forms.PasswordRecoveryForm import PasswordRecoveryForm
from .forms.ResetPasswordForm import ResetPasswordForm
from data.users import User
from data import db_session
from .mail.mail import send_mail

auth = Blueprint("auth", __name__, template_folder="../templates")


# Авторизация
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
            flash("Вы вошли в аккаунт!", category="success")
            return redirect(url_for('views.home'))
        flash("Неправильный логин или пароль.", category="error")
    return render_template("login.html", title='Авторизация', form=form, user=current_user)


# Регистрация
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if not current_user.is_anonymous:
        abort(404)
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash("Пароли не совпадают!", "warning")
            return render_template("signup.html", title='Регистрация', form=form, user=current_user)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash("Такой пользователь уже есть!", "warning")
            return render_template("signup.html", title='Регистрация', form=form, user=current_user)
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        flash("Вы зарегистрированы!", "success")
        return redirect(url_for('auth.login'))
    return render_template("signup.html", title='Регистрация', form=form, user=current_user)


# Выход из аккаунта
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта")
    return redirect("/")


# Восстановление пароля
@auth.route("/password_recovery", methods=['GET', 'POST'])
def password_recovery():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    
    form = PasswordRecoveryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        
        email = form.email.data
        
        user = db_sess.query(User).filter(User.email == email).first()
        
        if not user:
            flash("Что-то пошло не так... Возможно вы указали неверную почту", "error")
            return redirect(url_for('auth.login'))
        
        send_password_reset_email(user)
        flash("Письмо отправлено на почту!", "success")
        return redirect(url_for('auth.login'))
            
    return render_template("password_recovery.html", title="Сброс пароля", form=form, user=current_user)


# Отсылает письмо на указанную почту в user.email
def send_password_reset_email(user: User):
    token = user.get_reset_password_token()
    send_mail(user.email, "Восстановление пароля", html_body=render_template("email/email_template.html", user=user, token=token))


# Сбрасывает пароль
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    db_sess = db_session.create_session()
    user_id = User.verify_reset_password_token(token)
    
    if not user_id:
        return redirect(url_for('views.home'))
    
    user = db_sess.query(User).get(user_id)
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        
        user.set_password(form.password.data)
        db_sess.commit()
        
        flash('Ваш пароль сброшен!', "success")
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', title='Сброс пароля', user=current_user, form=form)