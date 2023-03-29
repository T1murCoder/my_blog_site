from flask import Blueprint, render_template
from data import db_session

views = Blueprint("views", __name__, template_folder="../templates")


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", title='Home')