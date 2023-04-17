from flask import Blueprint, render_template, flash, abort, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from requests import get
from data import db_session
from data.news_posts import NewsPost
from data.comments import Comment
from data.likes import Like
from data.users import User
from .forms.CreateCommentForm import CommentForm
from .forms.ChangePasswordForm import ChangePasswordForm

views = Blueprint("views", __name__, template_folder="../templates", static_url_path="../static")


@views.route("/")
@views.route("/home")
def home():
    db_sess = db_session.create_session()

    posts = db_sess.query(NewsPost).all()[::-1]

    return render_template("home.html", title='Home', posts=posts, user=current_user)


@views.route("/like/<int:post_id>", methods=['POST'])
@login_required
def like_post(post_id):
    db_sess = db_session.create_session()
    post = db_sess.query(NewsPost).get(post_id)
    if not post:
        flash('Такого поста ну существует!', 'danger')
        return jsonify({'error': 'Post does not exist.'}, 400)
    like = db_sess.query(Like).filter(Like.author_id == current_user.id, Like.post_id == post_id).first()
    if like:
        db_sess.delete(like)
        db_sess.commit()
    else:
        like = Like(
            author_id=current_user.id,
            post_id=post_id
        )
        db_sess.add(like)
        db_sess.commit()
    # back = request.referrer
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author_id, post.likes)})


@views.route("/posts/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    # TODO: Сделать отображение времени по другому
    form = CommentForm()
    db_sess = db_session.create_session()
    post = db_sess.query(NewsPost).get(post_id)
    if not post:
        flash("Такого поста не существует!", "danger")
        abort(404)
    if form.validate_on_submit():
        if not form.text.data:
            flash("Вы не указали текст комментария!", "Warning")
            return render_template("post_with_comments.html", title='View post', post=post, form=form, user=current_user)
        if len(form.text.data) > 200:
            flash("Комментарий слишком длинный!", "Warning")
            return render_template("post_with_comments.html", title='View post', post=post, form=form, user=current_user)
        comment = Comment(
            text=form.text.data,
            author_id=current_user.id,
            post_id=post_id
        )
        db_sess.add(comment)
        db_sess.commit()
        flash("Комментарий опубликован!", "success")
        return redirect(f"/posts/{post_id}")
        
    return render_template("post_with_comments.html", title='View post', post=post, form=form, user=current_user)


@views.route("/delete-comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).get(comment_id)
    if not comment:
        flash("Такого комментария не существует", "danger")
        abort(404)
    if current_user.id != comment.author_id and not current_user.admin:
        abort(404)
    post_id = comment.post_id
    db_sess.delete(comment)
    db_sess.commit()
    return redirect(url_for('views.view_post', post_id=post_id))


@views.route("/edit-comment/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    form = CommentForm()
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).get(comment_id)
    if not comment:
        flash("Такого комментария не существует", "danger")
        abort(404)
    if current_user.id != comment.author_id:
        abort(404)
    
    if form.validate_on_submit():
        comment.text = form.text.data
        db_sess.commit()
        return redirect(url_for('views.view_post', post_id=comment.post_id))
    form.text.data = comment.text
    
    return render_template("edit_comment.html", title='Edit comment', form=form, user=current_user)


@views.route("/profile")
@login_required
def view_profile():
    return render_template("user_profile.html", title='Профиль', user=current_user)

@views.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        old_password = form.old_password.data
        new_password = form.new_password.data
        repeat_new_password = form.repeat_new_password.data
        
        user = db_sess.query(User).get(current_user.id)
        if not user.check_password(old_password):
            flash("Вы ввели неправильный пароль!", "danger")
            return redirect(url_for('views.view_profile'))
        
        if new_password != repeat_new_password:
            flash("Пароли не совпадают!", "danger")
            return redirect(url_for('views.view_profile'))
        
        user.set_password(new_password)
        db_sess.commit()
        flash("Пароль успешно изменён!", "success")
        return redirect(url_for('views.view_profile'))
    return render_template("change_password.html", title='Изменение пароля', form=form, user=current_user)


@views.route('/change_avatar')
@login_required
def change_avatar():
    # Сделать форму
    return "Change avatar"