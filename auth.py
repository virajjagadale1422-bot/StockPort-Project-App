from flask import session, redirect, url_for
from models import validate_login, create_user

def login_user(username, password):
    user = validate_login(username, password)
    if user:
        session['user_id'] = user['id']
        return True
    return False

def register_user(username, password):
    create_user(username, password)

def check_user_logged_in():
    return 'user_id' in session
