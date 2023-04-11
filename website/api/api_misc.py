from flask import Blueprint, render_template, abort, redirect, url_for, jsonify
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
