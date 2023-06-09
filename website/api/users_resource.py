from flask import jsonify, current_app
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from .api_misc import admin_or_token_required
import os


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('admin', type=bool, default=False)
parser.add_argument('password', required=True)


# Если пользователь не существует
def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        current_app.logger.warning(f"User doesn't exist: id={user_id}")
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    @admin_or_token_required
    def get(self, user_id, **kwargs):
        abort_if_user_not_found(user_id)
        current_app.logger.info(f"'GET' request to [users] resource: user_id={user_id}")
        
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(user_id)
        return jsonify({'users': users.to_dict(only=('id', 'name', 'email', 'admin', 'about', 'hashed_password', 'created_date'))})
    
    @admin_or_token_required
    def delete(self, user_id, **kwargs):
        abort_if_user_not_found(user_id)
        current_app.logger.info(f"'DELETE' request to [users] resource: user_id={user_id}")
        
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        
        for comment in user.comments:
            if comment.images:
                images = comment.images.split('; ')
                # + Сделать редактирование
                for image in images:
                    os.remove("static/" + image)
                os.rmdir("static/" + '/'.join(image.split('/')[:-1]))
            db_sess.delete(comment)
    
        for like in user.likes:
            db_sess.delete(like)
        
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    @admin_or_token_required
    def get(self, **kwargs):
        current_app.logger.info(f"'GET' request to [users_list] resource")
        
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [item.to_dict(only=('id', 'name', 'email', 'admin', 'about', 'hashed_password', 'created_date')) for item in users]})
    
    @admin_or_token_required
    def post(self, **kwargs):
        args = parser.parse_args()
        
        current_app.logger.info(f"'POST' request to [users_list] resource: args=[{args}]")
        
        db_sess = db_session.create_session()
        user = User(
            name=args['name'],
            email=args['email'],
            admin=args['admin']
        )
        user.set_password(args['password'])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})