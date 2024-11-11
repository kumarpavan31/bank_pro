from flask import *
from .auth import *
from .model import *
from .images import *
from stitchtest.orders.model import TAILOR_ORDERS


tailor = Blueprint("tailor", __name__, static_folder="static", template_folder="templates")
tailor.secret_key = "jaffa"


@tailor.route("/", methods=["POST", "GET"])
def sign_in_page():
    return render_template("sign_in_page.html")


@tailor.route("/sign_up")
def sign_up_page():
    return render_template("sign_up_page.html")

@tailor.route("/set_price", methods=["POST", "GET"])
def set_pricing():
    tailor_id = request.args.get("tailor_id")
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
    return redirect(url_for("tailor.set_pricing", tailor_id=tailor_id))

@tailor.route("/validate_tailor", methods=["post"])
def validate_tailor():
    tailor_id = verify_tailor()
    if tailor_id == 0:
        flash("Invalid Credentials")
        return redirect(url_for("tailor.sign_in_page"))
    return render_template("tailor_dashboard.html", tailor_id=tailor_id)

@tailor.route("/home/<tailor_id>")
@tailor.route("/tailor_dashboard/<tailor_id>", methods= ["POST", "GET"])
def tailor_dashboard(tailor_id):
    return render_template("tailor_dashboard.html", tailor_id=tailor_id)

@tailor.route("/orders/<tailor_id>")
def tailor_orders(tailor_id):
    booking_orders = TAILOR_ORDERS().booking_orders(tailor_id)
    waiting_orders = TAILOR_ORDERS().waiting_orders(tailor_id)
    working_orders = TAILOR_ORDERS().working_orders(tailor_id)
    return render_template("tailor_orders.html", tailor_id=tailor_id, waiting_orders=waiting_orders, working_orders=working_orders, booking_orders=booking_orders)


@tailor.route("/sign_in/<tailor_id>", methods= ["post", "get"])
def index_page(tailor_id):
    return render_template("tailor_page.html", tailor_id=tailor_id)


@tailor.route("/cancel_order/<tailor_id>/<order_id>" , methods= ["POST", "GET"])
def cancel_order(tailor_id, order_id):

    return render_template("extend_to_cancel_orders.html", tailor_id=tailor_id, order_id=order_id)


@tailor.route("/reason_to_cancel/<tailor_id>/<order_id>")
def note_reason(tailor_id, order_id):
    note_reason_to_cancel(order_id)
    return redirect(url_for())


@tailor.route("/register")
def register_tailor():
    pass

