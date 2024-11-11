import random
import datetime
from stitchtest.tailor.model import TAILOR
from .model import *
from stitchtest.users.model import ADDRESS
from stitchtest.executive.model import DELIVERY_PARTNER


def create_order(user_id, tailor_id, garment, price, address):
    order_id = random.randint(a=220000000, b=229999999)
    tailor_address = TAILOR().tailor_info(tailor_id)[7]
    tailor_contact = TAILOR().tailor_info(tailor_id)[3]
    tailor_name = TAILOR().tailor_info(tailor_id)[1]
    ordered_on = datetime.datetime.now()
    import pdb;pdb.set_trace()
    get_address = ADDRESS().get_address(user_id, address)
    customer_address = get_address[5]
    customer_name = get_address[2]
    customer_contact = get_address[4]
    ORDERS().add_order(order_id, user_id, tailor_id, customer_address, customer_name, customer_contact, tailor_address, tailor_contact, tailor_name, garment, price, ordered_on)
    return order_id


def executive_select_order(order_id, executive_id):
    otp = random.randint(a=100000, b=999999)
    executive_info = DELIVERY_PARTNER().executive_details(executive_id)
    import pdb;pdb.set_trace()
    executive_name = executive_info[1]
    executive_contact = executive_info[3]
    ORDERS().update_status_waiting(order_id, otp, executive_id, executive_contact, executive_name)
    return