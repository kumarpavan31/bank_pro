from flask import *
from .auth import *
from .model import *
from .images import *


tailor = Blueprint("tailor", __name__, static_folder="static", template_folder="templates")


@tailor.route("/")
def sign_in_page():
    return render_template("sign_in_page.html")

@tailor.route("/sign_up")
def sign_up_page():
    return render_template("sign_up_page.html")

@tailor.route("/set_price", methods=["POST", "GET"])
def set_pricing(tailor_id = None):
    if request.method == "POST":
        tailor_id = sign_up_data()
        skills= SKILL().read_skills(tailor_id)
        return render_template("set_price.html", tailor_id=tailor_id, skills=skills)
    skills = SKILL().read_skills(tailor_id)
    return render_template("set_price.html", tailor_id=tailor_id, skills=skills)


@tailor.route("/add_price/<garment>/<tailor_id>", methods= ["POST", "GET"])
def add_price(garment, tailor_id):
    take_price(garment, tailor_id)
    flash("Price updated successfully")
    return redirect(url_for("set_pricing", tailor_id=tailor_id))



@tailor.route("/dashboard/<tailor_id>")
def tailor_dashboard(tailor_id):
    pass



@tailor.route("/sign_in/<tailor_id>")
def index_page(tailor_id):
    return render_template("tailor_page.html", tailor_id=tailor_id)


@tailor.route("/register")
def register_tailor():
    pass

