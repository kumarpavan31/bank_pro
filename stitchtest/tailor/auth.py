from flask import request
import random
import datetime
from .model import *
from .images import *


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
    price = request.form.get("price")
    SKILL().add_price(tailor_id, garment, price)
    return

