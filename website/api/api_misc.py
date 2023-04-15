from flask import Blueprint, render_template, abort, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps


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
    if token == 'test':
        return True
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