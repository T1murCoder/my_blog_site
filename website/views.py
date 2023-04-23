from flask import Blueprint, render_template, flash, abort, redirect, url_for, request, jsonify, current_app
from flask_login import login_required, current_user
from data import db_session
from data.news_posts import NewsPost
from data.comments import Comment
from data.likes import Like
from data.users import User
from data.feedback import Feedback
from .forms.CreateCommentForm import CommentForm
from .forms.ChangePasswordForm import ChangePasswordForm
from .forms.ChangeAvatarForm import ChangeAvatarForm
from .forms.ChangeAboutForm import ChangeAboutForm
from .forms.FeedbackForm import FeedbackForm
from datetime import datetime
from sqlalchemy import func
import os

views = Blueprint("views", __name__, template_folder="../templates", static_url_path="../static")


# Домашняя страница
@views.route("/")
@views.route("/home")
def home():
    db_sess = db_session.create_session()

    posts = db_sess.query(NewsPost).all()[::-1]

    return render_template("home.html", title='Home', posts=posts, user=current_user)


# Лайк поста (приходит 'POST' запрос с помощью JS)
@views.route("/like/<int:post_id>", methods=['POST'])
@login_required
def like_post(post_id):
    db_sess = db_session.create_session()
    post = db_sess.query(NewsPost).get(post_id)
    if not post:
        current_app.logger.warning(f"Post doesn't exist: post_id={post_id}")
        flash('Такого поста ну существует!', 'error')
        return jsonify({'error': 'Post does not exist.'}, 400)
    like = db_sess.query(Like).filter(Like.author_id == current_user.id, Like.post_id == post_id).first()
    if like:
        db_sess.delete(like)
        db_sess.commit()
        current_app.logger.debug(f"User has liked post: {current_user}; post_id={post.id}")
    else:
        like = Like(
            author_id=current_user.id,
            post_id=post_id
        )
        db_sess.add(like)
        db_sess.commit()
        current_app.logger.debug(f"User has unliked post: {current_user}; post_id={post.id}")
    # back = request.referrer
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author_id, post.likes)})


# Просмотр поста
@views.route("/posts/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    form = CommentForm()
    db_sess = db_session.create_session()
    post = db_sess.query(NewsPost).get(post_id)
    if not post:
        current_app.logger.warning(f"Post doesn't exist: post_id={post_id}")
        flash("Такого поста не существует!", "error")
        abort(404)
    if form.validate_on_submit():

        if len(form.text.data) > 200:
            flash("Комментарий слишком длинный!", "warning")
            return render_template("post_with_comments.html", title='View post', post=post, form=form, user=current_user)
        new_comment_id = db_sess.query(func.max(Comment.id)).first()[0] + 1
        
        if form.files.data:
            files = form.files.data
            file_names = []
            # тут сохраняются файлы по принципу "static/img/user/content/{id поста}/{id комментария}/{номер изображения}.jpg"
            for i, file in enumerate(files):
                filename = f"static/img/user/content/{post_id}/{new_comment_id}/{i + 1}.jpg"
                file_names.append(filename.split('/', 1)[1])
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                current_app.logger.info(f"User attached file: {current_user}; filename={filename}")
                
                with open(filename, 'wb') as f:
                    f.write(file.read())

        comment = Comment(
            text=form.text.data,
            author_id=current_user.id,
            post_id=post_id,
            images="; ".join(file_names)
        )
        db_sess.add(comment)
        db_sess.commit()
        current_app.logger.info(f"User has commented post: {current_user}; post_id={post.id}; comment_id={new_comment_id}")
        flash("Комментарий опубликован!", "success")
        return redirect(f"/posts/{post_id}")
        
    return render_template("post_with_comments.html", title='View post', post=post, form=form, user=current_user)


# Удаление комментария
@views.route("/delete-comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).get(comment_id)
    if not comment:
        current_app.logger.warning(f"Comment doesn't exist: comment_id={comment_id}")
        flash("Такого комментария не существует", "error")
        abort(404)
    if current_user.id != comment.author_id and not current_user.admin:
        current_app.logger.debug(f"User tried to delete someone else's comment: {current_user}; comment_id={comment_id}")
        abort(404)
    post_id = comment.post_id
    if comment.images:
        images = comment.images.split('; ')

        for image in images:
            os.remove("static/" + image)
        os.rmdir("static/" + '/'.join(image.split('/')[:-1]))
    db_sess.delete(comment)
    db_sess.commit()
    current_app.logger.info(f"User has deleted comment: {current_user}; post_id={post_id}; comment_id={comment_id}")
    flash("Комментарий удалён!", "success")
    return redirect(url_for('views.view_post', post_id=post_id))


# Редактирование комментария
@views.route("/edit-comment/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    form = CommentForm()
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).get(comment_id)
    if not comment:
        current_app.logger.warning(f"Comment doesn't exist: comment_id={comment_id}")
        flash("Такого комментария не существует", "error")
        abort(404)
    if current_user.id != comment.author_id:
        current_app.logger.debug(f"User tried to delete someone else's comment: {current_user}; comment_id={comment_id}")
        abort(404)
    
    if form.validate_on_submit():
        post_id = comment.post_id
        
        comment.text = form.text.data
        
        if comment.images:
            images = comment.images.split('; ')
            
            for image in images:
                os.remove("static/" + image)
            os.rmdir("static/" + '/'.join(image.split('/')[:-1]))
        
        files = form.files.data
        file_names = []
        
        for i, file in enumerate(files):
            if not file:
                continue
            filename = f"static/img/user/content/{post_id}/{comment_id}/{i + 1}.jpg"
            file_names.append(filename.split('/', 1)[1])
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            current_app.logger.info(f"User attached file: {current_user}; filename={filename}")
            
            with open(filename, 'wb') as f:
                f.write(file.read())
        
        comment.images = "; ".join(file_names)
        
        current_app.logger.info(f"User edited comment: {current_user}; comment_id={comment_id}")
        
        db_sess.commit()
        return redirect(url_for('views.view_post', post_id=comment.post_id))
    form.text.data = comment.text
    
    return render_template("edit_comment.html", title='Edit comment', comment=comment, form=form, user=current_user)


# Просмотр профиля
@views.route("/profile")
@login_required
def view_profile():
    current_app.logger.debug(f"User opened profile: {current_user}")
    return render_template("user_profile.html", title='Профиль', user=current_user)


# Изменение пароля
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
            current_app.logger.debug(f"User entered an incorrect password: {current_user}")
            flash("Вы ввели неправильный пароль!", "error")
            return redirect(url_for('views.view_profile'))
        
        if new_password != repeat_new_password:
            current_app.logger.debug(f"Passwords don't match: {current_user}")
            flash("Пароли не совпадают!", "error")
            return redirect(url_for('views.view_profile'))
        
        user.set_password(new_password)
        db_sess.commit()
        
        current_app.logger.info(f"User changed password: {current_user}")
        
        flash("Пароль успешно изменён!", "success")
        return redirect(url_for('views.view_profile'))
    return render_template("change_password.html", title='Изменение пароля', form=form, user=current_user)


# Изменение аватара
@views.route('/change_avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    form = ChangeAvatarForm()
    if form.validate_on_submit():
        image = request.files.get('avatar')

        with open(f"static/img/user/avatars/avatar_{current_user.id}.jpg", 'wb') as f:
            f.write(image.read())
        
        current_app.logger.info(f"User changed avatar: {current_user}")
        
        flash("Аватар успешно изменён!", "success")
        return redirect(url_for('views.view_profile'))
    return render_template("change_avatar.html", title="Изменение аватара", form=form, user=current_user)


# Конвертирует дату в "{количество времени} назад"
@views.app_template_filter("time_ago")
def time_ago(start_time):
    end_time = datetime.now()
    diff = datetime.now() - start_time
    
    seconds = diff.seconds + diff.days * 24 * 3600
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days
    months = end_time.month - start_time.month + 12 * (end_time.year - start_time.year)
    years = months // 12
    if years > 0:
        return f"{years} year(s) ago"
    elif months > 0:
        return f"{months} month(s) ago"
    elif days > 0:
        return f"{days} day(s) ago"
    elif hours > 0:
        return f"{hours} hour(s) ago"
    elif minutes > 0:
        return f"{minutes} minute(s) ago"
    else:
        return f"{seconds} second(s) ago"


# Изменение информации "О себе"
@views.route('/edit_about', methods=['GET', 'POST'])
@login_required
def edit_about():
    form = ChangeAboutForm()
    
    db_sess = db_session.create_session()
    
    
    if form.validate_on_submit():
        user = db_sess.query(User).get(current_user.id)
        user.about = form.about.data
        
        db_sess.commit()
        
        current_app.logger.info(f"User changed 'about': {current_user}")
        
        flash('Информация "О себе" изменена!', 'success')
        return redirect(url_for('views.view_profile'))
    
    form.about.data = current_user.about
    
    return render_template('change_about.html', title='О себе', form=form, user=current_user)


@views.route('/feedback', methods=['GET', 'POST'])
def send_feedback():
    form = FeedbackForm()
    
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        
        feedback = Feedback(
            text=form.feedback.data,
            author_id=current_user.id
        )
        
        db_sess.add(feedback)
        db_sess.commit()
        
        current_app.logger.info(f"User {current_user} has sent feedback: feedback_id={feedback.id}")
        
        flash("Обратная связь отправлена!", "success")
        return redirect(url_for('views.home'))
        
    return render_template("feedback.html", title='Обратная связь', form=form, user=current_user)