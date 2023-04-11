from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from ..admin import admin_required
from data.users import User
from .api_misc import token_required


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('admin', type=bool, default=False)
parser.add_argument('password', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    @admin_required
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(user_id)
        return jsonify({'users': users.to_dict(only=('id', 'name', 'email', 'admin', 'hashed_password', 'created_date'))})
    
    @admin_required
    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(user_id)
        db_sess.delete(users)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    @admin_required
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [item.to_dict(only=('id', 'name', 'email', 'admin', 'hashed_password', 'created_date')) for item in users]})
    
    @admin_required
    def post(self):
        args = parser.parse_args()
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


class UsersTokenResource(Resource):
    @token_required
    def get(self, user_id, params):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(user_id)
        return jsonify({'users': users.to_dict(only=('id', 'name', 'email', 'admin', 'hashed_password', 'created_date'))})
    
    @token_required
    def delete(self, user_id, params):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(user_id)
        db_sess.delete(users)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersTokenListResource(Resource):
    @token_required
    def get(self, params):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [item.to_dict(only=('id', 'name', 'email', 'admin', 'hashed_password', 'created_date')) for item in users]})
    
    @token_required
    def post(self, params):
        args = parser.parse_args()
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