from flask import Blueprint, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .forms.admin.CreatePostForm import CreatePostForm
from data import db_session

admin = Blueprint("admin", __name__, template_folder="../templates/admin")

@admin.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    
    if form.validate_on_submit():
        return "Post Created!"
    return render_template("create_post.html", title='Create post', form=form, user=current_user)