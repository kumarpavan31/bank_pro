from flask import Blueprint, render_template
from .auth import *
from model import *


executive = Blueprint("executive", __name__, static_folder="static", template_folder="templates")


@executive.route("/")
def executive_request():
    return render_template("executive_request.html")


@executive.route("/sign_up", methods = ["post", "get"])
def sign_up():
    return render_template("executive_sign_up.html")


@executive.route("/add_executive", methods= ["post", "get"])
def adding_executive():
    executive_id = add_executive()
    return render_template("executive_dashboard.html", executive_id=executive_id)

@executive.route("/validate_executive")
def validate_executive():
    executive_id = check_login()
    return render_template("executive_dashboard.html", executive_id=executive_id)

