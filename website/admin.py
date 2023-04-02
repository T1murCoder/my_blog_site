from flask import Blueprint, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .forms.admin.CreatePostForm import CreatePostForm
from data.news_posts import NewsPost
from data import db_session

admin = Blueprint("admin", __name__, template_folder="../templates/admin", static_folder="../static")


@admin.route('/')
@login_required
def admin_panel():
    return render_template('admin_panel.html', title="Admin panel", user=current_user)


@admin.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        url = form.post_url.data
        
        try:
            domain = url.split('/')[2]
        except IndexError:
            return "Это не ссылка!"
        
        if not (domain == "t.me" or domain == "telegram.me"):
            return "Вы указали неправильную ссылку!"
        
        url = url.split('/', 3)[-1]
        url_exists = db_sess.query(NewsPost).filter(NewsPost.post_tg_url == url).first()
        
        if url_exists:
            return "Такой пост уже есть!"
        
        post = NewsPost(
            post_tg_url=url
        )
        db_sess.add(post)
        db_sess.commit()
        return "Post Created!"
    return render_template("create_post.html", title='Create post', form=form, user=current_user)