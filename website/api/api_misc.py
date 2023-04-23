from flask import abort, current_app
from flask_login import current_user
from functools import wraps
from data import db_session
from data.tokens import Token


# Для доступа по токену
def token_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        params = kwargs.get('params')
        if not check_args(params):
            abort(404)
        return func(*args, **kwargs)
    return decorated_view


# Проверка аргументов
# Заготовка для будущего, если понадобятся дополнительные аргументы
def check_args(args: str):
    try:
        # TODO: Можно переделать в словарь через map
        if args[0] == "?":
            args.replace("?", "", 1)
        args = args.split('&')
        
        for arg in args:
            key, value = arg.split('=')
            if key == 'token':
                check = check_token(value)
        return check
    except:
        return abort(404)


       
# Проверка токена в базе данных
def check_token(token):
    # TODO: Тут проверять токен в бд
    db_sess = db_session.create_session()
    tokens = map(lambda x: x.token, db_sess.query(Token).all())
    if token == 'HEAD_TOKEN' or token in tokens:
        current_app.logger.info(f"Token [{token}] was user")
        return True
    current_app.logger.warning(f"Token [{token}] doesn't exist")
    return False


# Для доступа по токену или админке
def admin_or_token_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        print(kwargs)
        if not current_user.is_anonymous:
            if current_user.admin:
                return func(*args, **kwargs)
        params = kwargs.get('params')
        if check_args(params):
            return func(*args, **kwargs)
        abort(404)
    return decorated_view