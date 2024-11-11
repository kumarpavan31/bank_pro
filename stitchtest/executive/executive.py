from flask import Blueprint, render_template
from .auth import *
from .model import *
from stitchtest.orders.model import EXECUTIVE_ORDERS
from stitchtest.orders.auth import executive_select_order


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

@executive.route("/validate_executive", methods= ["post", "get"])
def validate_executive():
    executive_id = request.args.get("executive_id")
    if request.method== "POST":
        executive_id = check_login()
        if executive_id == 0:
            return redirect(url_for("executive.executive_request"))
        waiting_orders = EXECUTIVE_ORDERS().waiting_orders()
        working_orders = EXECUTIVE_ORDERS().working_orders(executive_id)
        to_deliver_to_tailor = EXECUTIVE_ORDERS().to_deliver_to_tailor(executive_id)
        return render_template("executive_dashboard.html", executive_id=executive_id, waiting_orders=waiting_orders, working_orders=working_orders, to_deliver_to_tailor=to_deliver_to_tailor)
    waiting_orders = EXECUTIVE_ORDERS().waiting_orders()
    working_orders = EXECUTIVE_ORDERS().working_orders(executive_id)
    to_deliver_to_tailor = EXECUTIVE_ORDERS().to_deliver_to_tailor(executive_id)
    return render_template("executive_dashboard.html", executive_id=executive_id, waiting_orders=waiting_orders,
                           working_orders=working_orders, to_deliver_to_tailor=to_deliver_to_tailor)


@executive.route("/take_order/<order_id>/<executive_id>", methods= ["post", "get"])
def select_order(order_id, executive_id):
    executive_select_order(order_id, executive_id)
    return redirect(url_for("executive.validate_executive", executive_id=executive_id))



@executive.route("/take_measurements/<order_id>/<user_id>/<garment>/<executive_id>/<measurements>", methods= ["post", "get"])
def measurements_or_material(order_id, user_id, garment, executive_id, measurements):
    verify_otp(order_id)
    if measurements != 'None':
        pass
    else:
        if garment == "shirt":
            return render_template("dimensions_shirt_executive.html", garment=garment, executive_id=executive_id,
                                   user_id=user_id, order_id=order_id)
        elif garment == "trousers":
            return render_template("dimensions_trousers_executive.html", garment=garment, executive_id=executive_id,
                                   user_id=user_id, order_id=order_id)
        elif garment == "kurta_men":
            return render_template("dimensions_kurta_men_executive.html", garment=garment, executive_id=executive_id,
                                   user_id=user_id, order_id=order_id)
        elif garment == "dhoti":
            return render_template("dimensions_dhoti_executive.html", garment=garment, executive_id=executive_id,
                                   user_id=user_id, order_id=order_id)
        elif garment == "blouse":
            return render_template("dimensions_blouse_executive.html", garment=garment, executive_id=executive_id,
                                   user_id=user_id, order_id=order_id)
        elif garment == "saree":
            return render_template("dimensions_saree_executive.html", garment=garment, executive_id=executive_id,
                                   user_id=user_id, order_id=order_id)
        elif garment == "blazer":
            return render_template("dimensions_blazer_executive.html", garment=garment, executive_id=executive_id,
                                   user_id=user_id, order_id=order_id)
        elif garment == "kurta_women":
            return render_template("dimensions_kurta_women_executive.html", garment=garment, executive_id=executive_id,
                                   user_id=user_id, order_id=order_id)



@executive.route("/update_measurements/<garment>/<executive_id>/<user_id>/<order_id>", methods= ["get", "post"])
def measurements_update(garment, executive_id, user_id, order_id):
    note_measurements(garment, executive_id, user_id, order_id)
    flash("measurements updated successfully")
    return redirect(url_for("executive.validate_executive", executive_id=executive_id))


@executive.route("/handover_to_tailor/<order_id>/<user_id>/<garment>/<executive_id>/<tailor_id>", methods= ["get", "post"])
def hand_over_to_tailor(order_id, user_id, garment, executive_id, tailor_id):
    verify_tailor_otp(order_id)
    ORDERS().update_status_inprogress(order_id)
    flash("Material handed over to tailor")
    return redirect(url_for("executive.validate_executive", executive_id=executive_id))




