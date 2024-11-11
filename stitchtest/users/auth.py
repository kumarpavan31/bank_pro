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
    try:
        user_id = USERS().verify_login_db(contact, password)
        return user_id
    except Exception:
        flash("Invalid Credentials")
        return 0


def new_address_details(user_id):
    import pdb;pdb.set_trace()
    name= request.form.get("name")
    address = request.form.get("address")
    contact = request.form.get("contact")
    email= request.form.get("email")
    address_id = random.randint(a=550000000, b=559999999)
    ADDRESS().add_address(user_id, address_id, name, email, contact, address)
    return


def note_selected_address(user_id):
    address_id = request.form.get("address_id")
    return address_id

def check_choice(user_id, tailor_id, garment, address):
    choice= request.form.get("choice")
    if choice == "other":
        return redirect(url_for("book_executive", user_id=user_id, tailor_id=tailor_id, garment=garment, address=address))
    elif choice == "wallet":
        return


def add_to_wallet(user_id):
    amount = request.form.get("wallet")
    wallet_amount = USERS().user_info(user_id)[7]
    wallet = float(amount) + float(wallet_amount)
    USERS().update_wallet(user_id, wallet)
    return