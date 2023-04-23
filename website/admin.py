from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, current_app
from functools import wraps
from flask_login import current_user
from .forms.admin.CreatePostForm import CreatePostForm
from .forms.admin.AnswerFeedbackForm import AnswerFeedbackForm
from data.news_posts import NewsPost
from data.tokens import Token
from data.users import User
from data.feedback import Feedback
import requests
from data import db_session
from werkzeug.security import gen_salt
from .system.config import url
from .mail.mail import send_mail

admin = Blueprint("admin", __name__, template_folder="../templates/admin", static_folder="../static")


# Для доступа по админке
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_anonymous and current_user.admin:
            return func(*args, **kwargs)
        else:
            abort(404)
    return decorated_view


# Админская панель
@admin.route('/')
@admin_required
def admin_panel():
    return render_template('admin_panel.html', title="Admin panel", user=current_user)


# Создание поста
@admin.route("/create-post", methods=['GET', 'POST'])
@admin_required
def create_post():
    form = CreatePostForm()
    
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        post_url = form.post_url.data
        
        try:
            domain = post_url.split('/')[2]
        except IndexError:
            current_app.logger.warning(f"Not url: {post_url}")
            flash("Это не ссылка!", "error")
            return render_template("create_post.html", title='Create post', form=form, user=current_user)
        
        if not (domain == "t.me" or domain == "telegram.me"):
            current_app.logger.warning(f"Uncorrect url: {post_url}")
            flash("Вы указали неправильную ссылку!", "error")
            return render_template("create_post.html", title='Create post', form=form, user=current_user)
        
        post_url = post_url.split('/', 3)[-1]
        url_exists = db_sess.query(NewsPost).filter(NewsPost.post_tg_url == post_url).first()
        
        if url_exists:
            current_app.logger.warning(f"Post already exists: url={post_url}")
            flash("Такой пост уже есть!", "warning")
            return render_template("create_post.html", title='Create post', form=form, user=current_user)
        
        post = NewsPost(
            post_tg_url=post_url)
        db_sess.add(post)
        db_sess.commit()
        
        current_app.logger.info(f"Post is published by {current_user}: post_id={post.id}; post_url={post_url}")
        
        flash("Пост опубликован!", "success")
        return redirect(url_for("admin.manage_posts"))
    return render_template("create_post.html", title='Create post', form=form, user=current_user)


# Просмотр постов от лица админа
@admin.route('/view-posts')
@admin_required
def view_posts():
    db_sess = db_session.create_session()
    
    posts = db_sess.query(NewsPost).all()[::-1]
    return render_template("view_posts.html", title='View posts', user=current_user, posts=posts)


# Удаление поста по id
@admin.route('/delete-post/<int:post_id>')
@admin_required
def delete_post(post_id):
    
    response = requests.delete(url + f"api/v2/posts/{post_id}/token={current_app.config['API_TOKEN']}")
    if response:
        current_app.logger.info(f"Post deleted by {current_user}: post_id={post_id};")
        flash("Пост удалён!", "success")
    else:
        current_app.logger.warning(f"Post doesn't exist: post_id={post_id}")
        flash("Такого поста не существует...", "error")
    
    back = request.referrer
    return redirect(back)


# Управление постами
@admin.route('/manage-posts')
@admin_required
def manage_posts():
    return render_template("manage_posts.html", title='Manage posts', user=current_user)


# Управление пользователями
@admin.route('/manage-users')
@admin_required
def manage_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return render_template("manage_users.html", title="Manage users", users=users, user=current_user)


# Управление токенами
@admin.route('/manage-tokens')
@admin_required
def manage_tokens():
    db_sess = db_session.create_session()
    tokens = db_sess.query(Token).all()
    return render_template("manage_tokens.html", title='Manage tokens', tokens=tokens,  user=current_user)


# Создание токена
@admin.route('/add_token')
@admin_required
def add_token():
    def generate_token():
        db_sess = db_session.create_session()
        tokens = map(lambda x: x.token, db_sess.query(Token).all())
        new_token = gen_salt(20)
        while new_token in tokens:
            new_token = gen_salt(20)
        return new_token
    
    db_sess = db_session.create_session()
    token = Token()
    token.set_token(generate_token())
    db_sess.add(token)
    db_sess.commit()
    
    current_app.logger.info(f"Token was created by {current_user}: token_id={token.id}")
    
    back = request.referrer
    return redirect(back)


# Удаление токена
@admin.route('/delete_token/<int:token_id>')
@admin_required
def delete_token(token_id):
    db_sess = db_session.create_session()
    token = db_sess.query(Token).get(token_id)
    if not token:
        current_app.logger.warning(f"Token doesn't exists: id={token_id}")
        flash("Такого токена не существует", "error")
        abort(404)
    db_sess.delete(token)
    current_app.logger.info(f"Token [{token.id}] was deleted by {current_user}")
    db_sess.commit()
    return redirect(url_for('admin.manage_tokens'))


# Изменение прав пользователя
@admin.route('/change_admin/<int:user_id>')
@admin_required
def change_admin_user(user_id):
    if user_id == 1 or user_id == current_user.id:
        current_app.logger.warning(f"User {current_user} tried to change rights [{user_id}]")
        abort(404)
    
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    
    if not user:
        current_app.logger.warning(f"User doesn't exist")
        flash("Такого пользователя не существует", "error")
        abort(404)
    
    user.admin = not user.admin
    current_app.logger.info(f"User's [{user.id}; {user.name}; {user.admin}] rights was changed by {current_user}")
    db_sess.commit()
    
    return redirect(url_for("admin.manage_users"))


# Удаление пользователя
@admin.route('/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    if user_id == 1 or user_id == current_user.id:
        current_app.logger.warning(f"User {current_user} tried to delete [{user_id}]")
        abort(404)
    
    response = requests.delete(url + f"api/v2/users/{user_id}/token={current_app.config['API_TOKEN']}")
    if response:
        current_app.logger.info(f"[{user_id}] was deleted by {current_user}")
        flash("Пользователь удалён!", "success")
    else:
        current_app.logger.warning(f"User doesn't exists: id={user_id}")
        flash("Такого пользователя не существует...", "error")
    
    return redirect(url_for("admin.manage_users"))


@admin.route('/feedback')
def view_feedback_list():
    db_sess = db_session.create_session()
    feedback_list = db_sess.query(Feedback).all()
    return render_template('feedback_list.html', title='Ответ на обратную связь', feedback_list=feedback_list, user=current_user)


@admin.route('/feedback/<int:feedback_id>', methods=['GET', 'POST'])
def view_feedback(feedback_id):
    form = AnswerFeedbackForm()
    
    db_sess = db_session.create_session()
    feedback = db_sess.query(Feedback).get(feedback_id)
    if not feedback:
        flash("Такого фидбека не существует", "error")
        abort(404)
    
    if form.validate_on_submit():
        try:
            message = form.answer_feedback.data
            send_mail(feedback.author.email, "Ответ на обратную связь", html_body=render_template("email/feedback_email_template.html", user_message=feedback.text, message=message, user=feedback.author))
            
            current_app.logger.info(f"Answer to feedback has been sent to {feedback.author.email} by admin {current_user}")
            
            flash("Ответ отправлен!", "success")
            db_sess.delete(feedback)
            db_sess.commit()
            return redirect(url_for("admin.view_feedback_list"))
        except TimeoutError:
            current_app.logger.warning(f"Something goes wrong, message was not sent: Timeout error")
            
            flash("Что-то пошло не так... Попробуйте позже", "error")
            return redirect(url_for("admin.view_feedback_list"))
    
    return render_template('answer_to_feedback.html', title='Ответ на обратную связь', feedback=feedback, form=form, user=current_user)