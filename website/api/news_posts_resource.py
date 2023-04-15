from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.news_posts import NewsPost
from .api_misc import admin_or_token_required


parser = reqparse.RequestParser()
parser.add_argument('url', required=True)


# Если пост не существует
def abort_if_post_not_found(post_id):
    session = db_session.create_session()
    post = session.query(NewsPost).get(post_id)
    if not post:
        abort(404, message=f"Post {post_id} not found")


class NewsPostsResource(Resource):
    @admin_or_token_required
    def get(self, post_id, **kwargs):
        abort_if_post_not_found(post_id)
        db_sess = db_session.create_session()
        post = db_sess.query(NewsPost).get(post_id)
        return jsonify({'posts': post.to_dict(only=('id', 'post_tg_url'))})
    
    @admin_or_token_required
    def delete(self, post_id, **kwargs):
        abort_if_post_not_found(post_id)
        db_sess = db_session.create_session()
        post = db_sess.query(NewsPost).get(post_id)
        
        comments = post.comments
        for comment in comments:
            db_sess.delete(comment)
        
        likes = post.likes
        for like in likes:
            db_sess.delete(like)
        
        db_sess.delete(post)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class NewsPostsListResource(Resource):
    @admin_or_token_required
    def get(self, **kwargs):
        db_sess = db_session.create_session()
        posts = db_sess.query(NewsPost).all()
        return jsonify({'posts': [item.to_dict(only=('id', 'post_tg_url')) for item in posts]})
    
    @admin_or_token_required
    def post(self, **kwargs):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        # TODO: Тут сделать проверка url
        '''
        post = NewsPost(
            post_tg_url=args['post_tg_url']
        )
        db_sess.add(post)
        db_sess.commit()
        '''
        return jsonify({'success': 'OK'})