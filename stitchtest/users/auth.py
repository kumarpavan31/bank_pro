from flask import request, flash, redirect, url_for
from .model import *
from .users import *
import random
import datetime


def get_user_data():
    name = request.form.get("name")
    contact = request.form.get("customer_contact")
    password = request.form.get("password")
    if contact in USERS().check_contact():
        flash("Contact Number Already Registered")
        return redirect(url_for("sign_up_page"))
    user_id = random.randint(a=110000000, b=119999999)
    created_on = datetime.datetime.now()
    USERS().add_customer(user_id, name, contact, password, created_on)
    return user_id


def check_user():
    contact= request.form.get("customer_contact")
    password = request.form.get("customer_password")
    if contact in USERS().check_contact():
        if USERS().verify_login(contact, password):
            user_id = USERS().verify_login(contact, password)
            return user_id
        flash("Password Incorrect")
        return redirect(url_for("sign_in_page"))
    flash("contact not registered")
    return redirect(url_for("sign_in_page"))