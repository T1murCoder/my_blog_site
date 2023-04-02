from flask import Blueprint, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.news_posts import NewsPost

views = Blueprint("views", __name__, template_folder="../templates")


@views.route("/")
@views.route("/home")
def home():
    db_sess = db_session.create_session()
    
    posts = db_sess.query(NewsPost).all()
    
    return render_template("home.html", title='Home', posts=posts, user=current_user)


@views.route("/like/<int:post_id>")
@login_required
def like_post(post_id):
    return str(post_id)