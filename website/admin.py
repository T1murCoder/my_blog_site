from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, current_app
from functools import wraps
from flask_login import current_user
from .forms.admin.CreatePostForm import CreatePostForm
from data.news_posts import NewsPost
from data.tokens import Token
from data.users import User
import requests
from data import db_session
from werkzeug.security import gen_salt
from .system.config import url

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
        url = form.post_url.data
        
        try:
            domain = url.split('/')[2]
        except IndexError:
            flash("Это не ссылка!", "error")
            return render_template("create_post.html", title='Create post', form=form, user=current_user)
        
        if not (domain == "t.me" or domain == "telegram.me"):
            flash("Вы указали неправильную ссылку!", "error")
            return render_template("create_post.html", title='Create post', form=form, user=current_user)
        
        url = url.split('/', 3)[-1]
        url_exists = db_sess.query(NewsPost).filter(NewsPost.post_tg_url == url).first()
        
        if url_exists:
            flash("Такой пост уже есть!", "warning")
            return render_template("create_post.html", title='Create post', form=form, user=current_user)
        
        post = NewsPost(
            post_tg_url=url)
        db_sess.add(post)
        db_sess.commit()
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
        flash("Пост удалён!", "success")
    else:
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

@admin.route('/manage-tokens')
@admin_required
def manage_tokens():
    db_sess = db_session.create_session()
    tokens = db_sess.query(Token).all()
    return render_template("manage_tokens.html", title='Manage tokens', tokens=tokens,  user=current_user)

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
    back = request.referrer
    return redirect(back)


@admin.route('/delete_token/<int:token_id>')
@admin_required
def delete_token(token_id):
    db_sess = db_session.create_session()
    token = db_sess.query(Token).get(token_id)
    if not token:
        flash("Такого токена не существует", "error")
        abort(404)
    db_sess.delete(token)
    db_sess.commit()
    return redirect(url_for('admin.manage_tokens'))


@admin.route('/change_admin/<int:user_id>')
@admin_required
def change_admin_user(user_id):
    if user_id == 1 or user_id == current_user.id:
        abort(404)
    
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    
    if not user:
        flash("Такого пользователя не существует", "error")
        abort(404)
    
    user.admin = not user.admin
    db_sess.commit()
    
    return redirect(url_for("admin.manage_users"))


@admin.route('/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    if user_id == 1 or user_id == current_user.id:
        abort(404)
    
    response = requests.delete(url + f"api/v2/users/{user_id}/token={current_app.config['API_TOKEN']}")
    if response:
        flash("Пользователь удалён!", "success")
    else:
        flash("Такого пользователя не существует...", "error")
    
    return redirect(url_for("admin.manage_users"))