from flask import request, flash
import random
import datetime
from .model import *
from .images import *
from stitchtest.orders.model import ORDERS


def sign_up_data():
    tailor_id = random.randint(a=100000, b=999999)
    name = request.form.get("tailor_name")
    email = request.form.get("tailor_email")
    contact = request.form.get("tailor_contact")
    password = request.form.get("tailor_password")
    experience = request.form.get("experience")
    machine = request.form.get("tailor_machine")
    address = request.form.get("address")
    gender = request.form.get("gender")
    wallet = 0
    created_on = datetime.datetime.now()
    garments = request.form.getlist("garment")
    #import pdb;pdb.set_trace()
    TAILOR().add_tailor(tailor_id, name, email, contact, password, experience, machine, address, gender, wallet, created_on)
    for garment in garments:
        price = 0
        image = IMAGE().garment(garment)
        #import pdb;pdb.set_trace()
        SKILL().add_skills(tailor_id, garment, price, image)
    return tailor_id

def take_price(garment, tailor_id):
    given_price = request.args.get("price")
    price = float(given_price)
    SKILL().add_price(tailor_id, garment, price)
    return


def verify_tailor():
    import pdb;pdb.set_trace()
    contact = request.form.get("tailor_contact")
    password = request.form.get("tailor_password")
    try:
        tailor_id = TAILOR().verify_tailor_db(contact, password)
        return tailor_id
    except Exception:
        flash("Invalid Credentials")
        return 0

def note_reason_to_cancel(order_id):
    reason = request.form.get("cancel_reason")
    ORDERS().cancel_the_order(order_id, reason)
