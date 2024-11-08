from flask import *

orders = Blueprint("orders", __name__, static_folder="static", template_folder="templates")


@orders.route("/users/book_now/<tailor_id>/<garment>")
def order_init(tailor_id, garment):
    pass
