from flask import Blueprint, render_template, abort, redirect, url_for, flash
from functools import wraps
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .forms.admin.CreatePostForm import CreatePostForm
from data.news_posts import NewsPost
from data import db_session

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
            flash("Это не ссылка!", "danger")
            return render_template("create_post.html", title='Create post', form=form, user=current_user)
        
        if not (domain == "t.me" or domain == "telegram.me"):
            flash("Вы указали неправильную ссылку!", "danger")
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
def delete_posts(post_id):
    return str(post_id)


# Управление постами
@admin.route('/manage-posts')
@admin_required
def manage_posts():
    return render_template("manage_posts.html", title='Manage posts', user=current_user)


# Управление пользователями
@admin.route('/manage-users')
@admin_required
def manage_users():
    return "Manage users"