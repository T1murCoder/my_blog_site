from flask import Flask, has_request_context, request
from data import db_session
from flask_login import LoginManager
from flask_restful import Api
from website.api import users_resource, news_posts_resource
from website.system.config import get_logging_dict_config
from data.users import User
from dotenv import load_dotenv
import logging
import logging.config
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "my_super_secret_key"
    app.config['API_TOKEN'] = os.getenv("API_TOKEN")
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    login_manager.login_message = "Пожалуйста, войдите в аккаунт"
    login_manager.login_message_category = "error"
    api = Api(app)
    
    logging.config.dictConfig(get_logging_dict_config())
    logger = logging.getLogger("app")
    app.logger = logger

    api.add_resource(users_resource.UsersListResource, '/api/v2/users', '/api/v2/users/<params>')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>', '/api/v2/users/<int:user_id>/<params>')
    api.add_resource(news_posts_resource.NewsPostsListResource, '/api/v2/posts', '/api/v2/posts/<params>')
    api.add_resource(news_posts_resource.NewsPostsResource, '/api/v2/posts/<int:post_id>', '/api/v2/posts/<int:post_id>/<params>')

    from website.views import views
    from website.auth import auth
    from website.admin import admin

    app.register_blueprint(views, url_prefix="")
    app.register_blueprint(auth, url_prefix="")
    app.register_blueprint(admin, url_prefix="/admin")
    
    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    return app


if __name__ == "__main__":
    db_session.global_init("db/users.db")
    load_dotenv()
    app = create_app()
    app.run(port=8080, host='127.0.0.1')