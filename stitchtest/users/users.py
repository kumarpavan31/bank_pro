from flask import render_template, Blueprint, session, request, redirect, url_for, make_response
from .auth import *
from .model import *
from stitchtest.tailor.model import SKILL



users = Blueprint("users", __name__, static_folder="static", template_folder="templates")
users.secret_key = "jaffa"

@users.route("/sign_in")
@users.route("/")
def sign_in_page():
    return render_template("user_sign_in_page.html")

@users.route("/sign_up")
def sign_up_page():
    return render_template("user_sign_up_page.html")


@users.route("/register", methods=["POST", "GET"])
def add_user(user_id = None):
    services = SKILL().available_skills()
    if request.method == "POST":
        user_id = get_user_data()
        services = SKILL().available_skills()
        return render_template("user_index.html", user_id=user_id, services=services)
    return render_template("user_index.html", user_id=user_id, services=services)

@users.route("/home/<user_id>", methods=["get"])
@users.route("/validate_customer", methods = ["POST"])
def login_check(user_id = None):
    if request.method == "POST":
        user_id = check_user()
        services = SKILL().available_skills()
        return render_template("user_index.html", user_id=user_id, services=services)
    services = SKILL().available_skills()
    return render_template("user_index.html", user_id=user_id, services=services)

@users.route("/available_tailors/<garment>/<user_id>", methods= ["post", "get"])
def available_tailors(garment, user_id):
    available_tailors = SKILL().available_tailor(garment)
    return render_template("tailors_for_user.html", available_tailors=available_tailors, garment=garment, user_id = user_id)


@users.route("/selected_tailor/<garment>/<tailor_id>/<tailor_name>/<user_id>")
def about_tailor(garment, tailor_id, tailor_name, user_id):
    tailor_skills = SKILL().read_skills(tailor_id)
    return render_template("tailor_skills.html", tailor_id=tailor_id, tailor_skills=tailor_skills, garment=garment, tailor_name=tailor_name, user_id=user_id)


@users.route("/book_now/<tailor_id>/<garment>/<user_id>")
def select_address(tailor_id, garment, user_id):
    addresses = ADDRESS().get_all_address(user_id)
    return render_template("select_address.html", tailor_id=tailor_id, garment=garment, user_id=user_id, addresses=addresses)

@users.route("/new_address/<user_id>/<garment>/<tailor_id>")
def new_address(user_id, garment, tailor_id):
    addresses = ADDRESS().get_all_address(user_id)
    return render_template("new_address_block.html", user_id=user_id, garment=garment, tailor_id=tailor_id, addresses=addresses)


@users.route("/profile/<user_id>")
def view_user_profile(user_id):
    pass


@users.route("/orders/<user_id>")
def view_orders(user_id):
    pass

@users.route("/logout/<user_id>")
def user_logout():
    return redirect(url_for("opening_page"))