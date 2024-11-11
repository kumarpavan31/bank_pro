from flask import render_template, Blueprint, session, request, redirect, url_for, make_response, flash
from stitchtest.users.auth import *
from stitchtest.users.model import *
from stitchtest.tailor.model import SKILL
from stitchtest.orders.auth import create_order
from stitchtest.orders.model import CUSTOMER_ORDERS, ORDERS




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

@users.route("/validate_customer", methods = ["POST", "GET"])
def login_check():
    user_id = request.args.get("user_id")
    if request.method == "POST":
        user_id = check_user()
        if user_id == 0:
            return redirect(url_for("users.sign_in_page"))
        services = SKILL().available_skills()
        return render_template("user_index.html", user_id=user_id, services=services)
    services = SKILL().available_skills()
    return render_template("user_index.html", user_id=user_id, services=services)

@users.route("/home/<user_id>")
def user_home(user_id):
    return redirect(url_for("users.login_check", user_id=user_id))

@users.route("/available_tailors/<garment>/<user_id>", methods= ["post", "get"])
def available_tailors(garment, user_id):
    available_tailors = SKILL().available_tailor(garment)
    return render_template("tailors_for_user.html", available_tailors=available_tailors, garment=garment, user_id = user_id)


@users.route("/selected_tailor/<garment>/<tailor_id>/<tailor_name>/<user_id>", methods= ["post", "get"])
def about_tailor(garment, tailor_id, tailor_name, user_id):
    tailor_skills = SKILL().read_skills(tailor_id)
    return render_template("tailor_skills.html", tailor_id=tailor_id, tailor_skills=tailor_skills, garment=garment, tailor_name=tailor_name, user_id=user_id)


@users.route("/book_now/<tailor_id>/<garment>/<user_id>", methods= ["post", "get"])
def select_address(tailor_id, garment, user_id):
    email = USERS().user_info(user_id)[2]
    addresses = ADDRESS().get_all_address(user_id)
    return render_template("select_address.html", tailor_id=tailor_id, garment=garment, user_id=user_id, addresses=addresses, email = email)

@users.route("/new_address/<user_id>/<garment>/<tailor_id>", methods= ["post", "get"])
def new_address(user_id, garment, tailor_id):
    email = USERS().user_info(user_id)[2]
    addresses = ADDRESS().get_all_address(user_id)
    return render_template("extend_select_address.html", user_id=user_id, garment=garment, tailor_id=tailor_id, addresses=addresses, email=email)


@users.route("/add_address/<user_id>/<garment>/<tailor_id>", methods= ["post", "get"])
def add_new_address(user_id, garment, tailor_id):
    email = USERS().user_info(user_id)[2]
    new_address_details(user_id)
    return redirect(url_for("users.select_address", tailor_id=tailor_id, garment=garment, user_id=user_id, email=email))


@users.route("/decide_measurements/<user_id>/<tailor_id>/<garment>", methods= ["post", "get"])
def decide_measurements(user_id, tailor_id, garment):
    address_id = note_selected_address(user_id)
    return render_template("measurements.html", user_id=user_id, tailor_id=tailor_id, garment=garment, address=address_id)


@users.route("/book_tailor_to_measure/<user_id>/<tailor_id>/<garment>/<address>", methods= ["post", "get"])
def book_executive(user_id, tailor_id, garment, address):
    price = SKILL().get_price(tailor_id, garment)[0]
    return render_template("payment_page.html", user_id=user_id, tailor_id=tailor_id, garment=garment, address=address, price=price)

@users.route("/pay_now/<user_id>/<tailor_id>/<garment>/<price>/<address>", methods= ["post", "get"])
def pay_method(user_id, tailor_id, garment, price, address):
    check_choice(user_id, tailor_id, garment, address)  # comes here only when wallet is selected in the previous page
    wallet = USERS().user_info(user_id)[7]
    import pdb;pdb.set_trace()
    if float(price) > float(wallet):
        flash("Insufficient funds")
        return redirect(url_for("users.book_executive", user_id= user_id, tailor_id=tailor_id, garment=garment, address=address))
    order_id = create_order(user_id, tailor_id, garment, price, address)
    new_wallet = float(wallet) - float(price)
    USERS().update_wallet(user_id, new_wallet)
    return render_template("thank_you.html", user_id=user_id, order_id=order_id)


@users.route("/profile/<user_id>", methods=["get", "post"])
def view_user_profile(user_id):
    user_info = USERS().user_info(user_id)
    return render_template("user_profile.html", user_info=user_info, user_id=user_id)

@users.route("/add_amount/<user_id>")
def add_money(user_id):
    user_info = USERS().user_info(user_id)
    return render_template("extend_user_profile.html", user_id=user_id, user_info=user_info)



@users.route("/add_money_to_wallet/<user_id>", methods=["post"])
def add_money_to_wallet(user_id):
    add_to_wallet(user_id)
    return redirect(url_for("users.view_user_profile", user_id=user_id))

@users.route("/orders/<user_id>")
def view_orders(user_id):
    waiting_orders = CUSTOMER_ORDERS().waiting_orders(user_id)
    in_transit_orders = CUSTOMER_ORDERS().in_transit_orders(user_id)
    delivered_orders = CUSTOMER_ORDERS().delivered_orders(user_id)
    return render_template("users_orders.html", waiting_orders=waiting_orders, in_transit_orders=in_transit_orders, delivered_orders=delivered_orders, user_id=user_id)

@users.route("/logout/<user_id>")
def user_logout():
    return redirect(url_for("opening_page"))