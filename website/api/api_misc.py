from flask import Blueprint, render_template, abort, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps


def token_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        print(kwargs)
        params = kwargs.get('params')
        if not check_args(params):
            abort(404)
        return func(*args, **kwargs)
    return decorated_view


def check_args(args):
    try:
        # TODO: Можно переделать в словарь через map
        args = args.split('&')
        
        for arg in args:
            key, value = arg.split('=')
            if key == 'token':
                check = check_token(value)
        return check
    except:
        return abort(404)
            

def check_token(token):
    # Тут проверять токен в бд
    if token == 'test':
        return True
    return False


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