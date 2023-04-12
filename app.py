from flask import Flask
from data import db_session
from os import path
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource
from website.api import users_resource
from data.users import User


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "my_super_secret_key"
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    api = Api(app)

    api.add_resource(users_resource.UsersListResource, '/api/v2/users', '/api/v2/users/<params>')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>', '/api/v2/users/<int:user_id>/<params>')

    from website.views import views
    from website.auth import auth
    from website.admin import admin

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/admin")
    
    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    return app






if __name__ == "__main__":
    db_session.global_init("db/users.db")
    app = create_app()
    app.run(port=8080, host='127.0.0.1')