from flask import Blueprint, render_template, abort, redirect, url_for
from functools import wraps
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .forms.admin.CreatePostForm import CreatePostForm
from data.news_posts import NewsPost
from data import db_session

admin = Blueprint("admin", __name__, template_folder="../templates/admin", static_folder="../static")


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.admin:
            return func(*args, **kwargs)
        else:
            abort(404)
    return decorated_view


@admin.route('/')
@login_required 
@admin_required
def admin_panel():
    return render_template('admin_panel.html', title="Admin panel", user=current_user)


@admin.route("/create-post", methods=['GET', 'POST'])
@login_required
@admin_required
def create_post():
    form = CreatePostForm()
    
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        url = form.post_url.data
        
        try:
            domain = url.split('/')[2]
        except IndexError:
            return render_template("create_post.html", title='Create post', form=form, message="Это не ссылка!", user=current_user)
        
        if not (domain == "t.me" or domain == "telegram.me"):
            return render_template("create_post.html", title='Create post', form=form, message="Вы указали неправильную ссылку!", user=current_user)
        
        url = url.split('/', 3)[-1]
        url_exists = db_sess.query(NewsPost).filter(NewsPost.post_tg_url == url).first()
        
        if url_exists:
            return render_template("create_post.html", title='Create post', form=form, message="Такой пост уже есть!", user=current_user)
        
        post = NewsPost(
            post_tg_url=url)
        db_sess.add(post)
        db_sess.commit()
        return redirect(url_for("admin.manage_posts"))
    return render_template("create_post.html", title='Create post', form=form, user=current_user)


@admin.route('/view-posts')
@login_required
@admin_required
def view_posts():
    db_sess = db_session.create_session()
    
    posts = db_sess.query(NewsPost).all()[::-1]
    return render_template("view_posts.html", title='View posts', user=current_user, posts=posts)


@admin.route('/delete-post/<int:post_id>')
@login_required
@admin_required
def delete_posts(post_id):
    return str(post_id)


@admin.route('/manage-posts')
@login_required
@admin_required
def manage_posts():
    return render_template("manage_posts.html", title='Manage posts', user=current_user)


@admin.route('/manage-users')
@login_required
@admin_required
def manage_users():
    return "Manage users"