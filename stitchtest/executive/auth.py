import datetime

from flask import request, redirect, url_for, flash
from stitchtest.tailor.model import TAILOR
from .model import DELIVERY_PARTNER
import random
from stitchtest.orders.model import ORDERS
from stitchtest.users.model import MEASUREMENTS

def check_login():
    contact = request.form.get("contact")
    password = request.form.get("password")
    try:
        executive_id = DELIVERY_PARTNER().verify_login(contact, password)
        flash("Logged in successfully")
        return executive_id
    except Exception:
        flash("Invalid Credentials")
        return 0


def add_executive():
    name = request.form.get("name")
    email = request.form.get("email")
    contact= request.form.get("contact")
    password = request.form.get("password")
    address = request.form.get("address")
    executive_id = random.randint(a= 88000000, b=88999999)
    created_on = datetime.datetime.now()
    if contact in TAILOR().check_contact():
        flash("user registered as tailor")
        return redirect(url_for("executive.executive_request"))
    elif contact in DELIVERY_PARTNER().check_contact():
        flash("User Already registered as executive")
        return redirect(url_for("sign_up"))
    DELIVERY_PARTNER().add_executive(executive_id, name, email, contact, password, address, created_on)
    return executive_id



def verify_otp(order_id):
    customer_otp = request.form.get("customer_otp")
    order_info = ORDERS().define_order(order_id)
    if int(customer_otp) != order_info[0][17]:
        flash("Invalid OTP")
        return redirect(url_for("executive.validate_executive"))
    return


def note_measurements(garment, executive_id, user_id, order_id):
    form_data = request.form
    measurements = "\n".join([f"{key}: {value}" for key, value in form_data.items()])
    MEASUREMENTS().add_measurements(user_id, garment, measurements)
    otp = random.randint(a=100000, b=999999)
    ORDERS().update_measurements(order_id, measurements, otp)
    return

def verify_tailor_otp(order_id):
    tailor_otp = request.form.get("tailor_otp")
    order_info = ORDERS().define_order(order_id)
    if tailor_otp != order_info[18]:
        flash("Invalid OTP")
        return redirect(url_for("executive.validate_executive"))
    return