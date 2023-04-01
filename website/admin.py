from flask import Blueprint, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session

admin = Blueprint("admin", __name__, template_folder="../templates")

@admin.route("/test")
def test_admin():
    return "Test"