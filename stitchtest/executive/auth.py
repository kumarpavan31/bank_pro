import datetime

from flask import request, redirect, url_for, flash
from stitchtest.tailor.model import TAILOR
from .model import DELIVERY_PARTNER
import random

def check_login():
    contact = request.form.get("contact")
    password = request.form.get("password")
    if DELIVERY_PARTNER().verify_login(contact, password):
        executive_id = DELIVERY_PARTNER().verify_login(contact, password)
        flash("Logged in successfully")
        return executive_id
    flash("Invalid Credentials")
    return redirect(url_for("executive_request"))


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
        return redirect(url_for("executive_request"))
    elif contact in DELIVERY_PARTNER().check_contact():
        flash("User Already registered as executive")
        return redirect(url_for("sign_up"))
    DELIVERY_PARTNER().add_executive(executive_id, name, email, contact, password, address, created_on)
    return executive_id