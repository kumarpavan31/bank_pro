from flask import *
import datetime
import random
from tailor_model import *
from tailorimage import *
from customer_model import *
from order_model import *

import base64



app = Flask(__name__)
app.secret_key = "pakodi"

def b64encode(data):
    return base64.b64encode(data).decode('utf-8')
app.jinja_env.filters['b64encode'] = b64encode

@app.route("/", methods=["post", "get"])
def open_page():
    services= read_all_skill()
    return render_template("open_page.html", services=services)


@app.route("/tailorsignin")
def tailor_sign_in_page():
    return render_template("tailor_sign_in_page.html")
@app.route("/tailor_sign_up")
def tailor_sign_up_page():
    return render_template("tailor_sign_up_page.html")

@app.route("/set_price", methods=["get", "post"])
def register_tailor():
    import pdb;pdb.set_trace()
    if request.method=="POST":
        tailor_id = random.randint(a=100000, b=999999)
        tailor_name = request.form.get("tailor_name")
        tailor_email = request.form.get("tailor_email")
        tailor_contact = request.form.get("tailor_contact")
        tailor_password = request.form.get("tailor_password")
        experience = request.form.get("experience")
        tailor_machine = request.form.get("tailor_machine")
        address = request.form.get("address")
        gender = request.form.get("gender")
        revenue= 0
        created_on = datetime.datetime.now()
        shirt = request.form.get("shirt")
        trousers = request.form.get("trousers")
        kurta_men = request.form.get("kurta_men")
        dhoti = request.form.get("dhoti")
        blouse = request.form.get("blouse")
        saree = request.form.get("saree")
        blazer = request.form.get("blazer")
        kurta_women = request.form.get("kurta_women")
        minor_stitches = request.form.get("minor_stitches")
        custom = request.form.get("custom")
        shirt_image = image_shirt()
        trouser_image = image_trouser()
        kurta_men_image= image_kurta_men()
        dhoti_image= image_dhoti()
        blouse_image= image_blouse()
        saree_image= image_saree()
        blazer_image= image_blazer()
        kurta_women_image= image_kurta_women()
        minor_stitch_image= image_minor_stitch()
        custom_image= image_custom()
        value = 0
        try:
            register_tailor_db(tailor_id, tailor_name, tailor_email, tailor_contact, tailor_password, experience, tailor_machine, address, gender, revenue, created_on)
        except Exception as e:
            flash("email is already registered")
            return redirect(url_for("register_tailor"))
        add_tailor_skill(tailor_id,value, shirt, trousers, kurta_men, dhoti, blouse, saree, blazer, kurta_women, minor_stitches, custom, shirt_image, trouser_image, kurta_men_image, dhoti_image, blouse_image, saree_image, blazer_image, kurta_women_image, minor_stitch_image, custom_image)
        flash("Your account has been created successfully")
        session["tailor_id"]= tailor_id
        skills = read_tailor_skill(tailor_id)
        return render_template("set_price.html",skills=skills, tailor_id=tailor_id)
    else:
        tailor_id= session.get("tailor_id")
        skills = read_tailor_skill(tailor_id)
        return render_template("set_price.html",skills=skills, tailor_id=tailor_id)

@app.route("/set_value/<skill_name>/<tailor_id>", methods=["get", "post"])
def set_value(skill_name, tailor_id):
    #import pdb;pdb.set_trace()
    value= request.args.get("value")
    set_price_tailor(skill_name, tailor_id, value)
    return redirect(url_for("register_tailor"))


@app.route("/sign_in_tailor", methods=["post", "get"])
def tailor_sign_in():
    if request.method== "POST":
        session.pop("tailor_id")
        flash("Your Registration has been Successfully completed. Continue to login")
        return render_template("tailor_sign_in_page.html")
    return render_template("tailor_sign_in_page.html")

@app.route("/validate_tailor", methods=["post", "get"])
def check_login_tailor():
    if request.method=="POST":
        tailor_contact= request.form.get("tailor_contact")
        tailor_password = request.form.get("tailor_password")
        tailor_details = check_tailor(tailor_contact)
        if tailor_details and tailor_password== tailor_details[5]:
            session["tailor_id"]= tailor_details[1]
            tailor_id = session.get("tailor_id")
            unpaid_orders = unpaid_orders_db(tailor_id)
            working_orders = tailor_orders(tailor_id)
            delivered_orders = tailor_paid_orders(tailor_id)
            return render_template("tailor_dashboard.html", unpaid_orders=unpaid_orders, working_orders=working_orders, delivered_orders=delivered_orders)
        flash("invalid Credentials")
        return redirect(url_for("tailor_sign_in_page"))
    tailor_id = session.get("tailor_id")
    working_orders = tailor_orders(tailor_id)
    delivered_orders = tailor_paid_orders(tailor_id)
    unpaid_orders = unpaid_orders_db(tailor_id)
    return render_template("tailor_dashboard.html", unpaid_orders=unpaid_orders, working_orders=working_orders, delivered_orders=delivered_orders)
@app.route("/all_tailors_for/<skill_name>")
def all_tailors_for(skill_name):
    all_ids = all_tailor_ids(skill_name)
    ids= all_ids[0]
    tailor_dict = {}
    results= get_tailors_with_skills(skill_name)
    for tailor_id, tailor_name, skill_name in results:
        if tailor_id not in tailor_dict:
            tailor_dict[tailor_id] = {
                'name': tailor_name,
                'skills': []
            }
        if skill_name:  # Ensure skill_name is not None
            tailor_dict[tailor_id]['skills'].append({
                'skill_name': skill_name
            })
    return render_template("available_tailors.html", tailor_dict=tailor_dict)

@app.route("/customer_sign_in")
def customer_sign_in_page():
    return render_template("customer_sign_in_page.html")

@app.route("/customer_sign_up")
def customer_sign_up_page():
    return render_template("customer_sign_up_page.html")

@app.route("/cust_sign_up", methods=["GET", "POST"])
def customer_sign_up():
    if request.method == "POST":
        customer_id = random.randint(a=10000000, b=99999999)
        customer_name = request.form.get("name")
        customer_contact = request.form.get("customer_contact")
        customer_password = request.form.get("password")
        wallet = 2000
        created_on = datetime.datetime.now()
        try:
            add_customer_db(customer_id, customer_name, customer_contact, customer_password, wallet, created_on)
        except:
            flash("Contact NUmber is already registered")
            return redirect(url_for("customer_sign_up_page"))
        session["customer_id"] = customer_id
        services = read_all_skill()
        return render_template("customer_entry_page.html", customer_id=customer_id, services=services)
    services = read_all_skill()
    customer_id = session.get("customer_id")
    return render_template("customer_entry_page.html", customer_id=customer_id, services=services)

@app.route("/all_tailors_for/<skill_name>/<customer_id>")
def all_tailors_for_cust(skill_name, customer_id):
    #all_ids = all_tailor_ids(skill_name)
    #ids= all_ids[0]
    tailor_dict = {}
    results= get_tailors_with_skills(skill_name)
    for tailor_id, tailor_name, skill_name in results:
        if tailor_id not in tailor_dict:
            tailor_dict[tailor_id] = {
                'name': tailor_name,
                'skills': []
            }
        if skill_name:  # Ensure skill_name is not None
            tailor_dict[tailor_id]['skills'].append({
                'skill_name': skill_name
            })
    return render_template("available_tailors_cust.html", tailor_dict=tailor_dict, customer_id=customer_id)


@app.route("/cust_profile/<customer_id>")
def customer_profile_page(customer_id):
    cust_details = read_customer_db(customer_id)
    return render_template("customer_profile.html", customer_id=customer_id, cust_details=cust_details)


@app.route("/custhome/<customer_id>")
def customer_home(customer_id):
    return redirect(url_for("customer_sign_up", customer_id=customer_id))


@app.route("/validate_customer", methods= ["get", "post"])
def customer_sign_in():
    customer_contact = request.form.get("customer_contact")
    customer_password = request.form.get("customer_password")
    cust_data = check_customer_db(customer_contact, customer_password)
    if cust_data:
        session["customer_id"] = cust_data[1]
        flash("logged in successfully")
        return redirect(url_for("customer_sign_up"))
    flash("Invalid Credentials")
    return redirect(url_for("customer_sign_in_page"))


@app.route("/edit_cust_profile/<customer_id>", methods=["get", "post"])
def edit_customer_profile(customer_id):
    cust_details = read_customer_db(customer_id)
    return render_template("edit_profile.html", customer_id=customer_id, cust_details=cust_details)


@app.route("/edit_all_data/<customer_id>")
def change_cust_profile(customer_id):
    customer_name= request.form.get("customer_name")
    customer_email = request.form.get("customer_email")
    address = request.form.get("address")
    update_customer(customer_id, customer_name, customer_email, address)
    flash("Profile Updated successfully")
    return redirect(url_for("customer_sign_up"))

@app.route("/add_money/<customer_id>")
def add_money(customer_id):
    cust_details = read_customer_db(customer_id)
    return render_template("extend_cust_profile.html", customer_id=customer_id, cust_details=cust_details)

@app.route("/add_tp_wallet/<customer_id>")
def add_to_wallet(customer_id):
    amount= request.form.get("amount")
    cust_detail = read_customer_db(customer_id)
    wallet = int(cust_detail[8]) + int(amount)
    add_money_to_wallet(customer_id, wallet)
    flash("Amount added to wallet")
    return redirect(url_for("customer_profile_page", customer_id=customer_id))

@app.route("/about_tailor/<tailor_id>/<customer_id>")
def about_tailor(tailor_id, customer_id):
    skills = about_tailor_skills(tailor_id)
    tailor_name = about_tailor_db(tailor_id)[2]
    return render_template("price_list_tailor.html", skills=skills, customer_id=customer_id, tailor_name=tailor_name, tailor_id=tailor_id)

@app.route("/booking/<tailor_id>/<customer_id>")
def try_to_book(tailor_id, customer_id):
    skills = about_tailor_skills(tailor_id)
    tailor_name = about_tailor_db(tailor_id)[2]
    return render_template("booking_page.html", tailor_id=tailor_id, customer_id=customer_id, tailor_name=tailor_name, skills=skills)

@app.route("/procced_dimensions/<tailor_id>/<customer_id>", methods=["GET", "POST"])
def cust_dimensions(tailor_id, customer_id):
    choice = request.form.get("choice")
    if choice =="minor_stitches" or "custom":
        pass

    return render_template("dimensions.html", tailor_id=tailor_id, customer_id=customer_id, choice=choice)

@app.route("/cust_orders/<customer_id>")
def cust_orders(customer_id):
    unpaid_orders = unpaid_orders_customer(customer_id)
    pending_orders = customer_progress_orders(customer_id)
    completed_orders = customer_completed_orders(customer_id)
    return render_template("customer_orders.html", customer_id=customer_id, unpaid_orders=unpaid_orders, pending_orders=pending_orders, completed_orders=completed_orders)


@app.route("/payment_after_measurement/<garment>/<customer_id>/<tailor_id>/<temp_orderid>", methods=["POST", "GET"])
def try_to_pay(garment, customer_id, tailor_id, temp_orderid):
    measurements= request.form.get("measurements")
    if measurements:
        return redirect(url_for("payment_page", customer_id=customer_id, tailor_id=tailor_id, choice=garment, temp_orderid=temp_orderid))
    flash("Measurements not updated by tailor")
    return redirect(url_for("cust_orders", customer_id=customer_id))


@app.route("/self_customize/<choice>/<tailor_id>/<customer_id>", methods=["GET", "POST"])
def self_measure(choice, tailor_id, customer_id):
    if choice== "shirt":
        return render_template("dimensions_shirt.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)
    elif choice=="trousers":
        return render_template("dimensions_trouser.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)
    elif choice=="kurta_men":
        return render_template("dimensions_kurta_men.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)
    elif choice=="dhoti":
        return render_template("dimensions_dhoti.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)
    elif choice=="blouse":
        return render_template("dimensions_blouse.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)
    elif choice=="saree":
        return render_template("dimensions_saree.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)
    elif choice=="blazer":
        return render_template("dimensions_blazer.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)
    elif choice=="kurta_women":
        return render_template("dimensions_kurta_women.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)
    elif choice=="minor_stitches":
        return render_template("dimensions_minor_stitches.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)
    elif choice=="custom":
        return render_template("dimensions_custom.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)

@app.route("/take_order/<choice>/<tailor_id>/<customer_id>" , methods=["GET", "POST"])
def taking_order(choice, tailor_id, customer_id):
    import pdb;pdb.set_trace()

    if request.method=="POST":
        form_data = request.form
        form_text = "\n".join([f"{key}: {value}" for key, value in form_data.items()])
        measurements = form_text
        order_created = datetime.datetime.now()
        cust_details = read_customer_db(customer_id)
        cust_name = cust_details[0][2]
        customer_contact= cust_details[0][4]
        customer_address= cust_details[0][6]
        if customer_address is None:
            return render_template("add_address_to_order.html", customer_id=customer_id, tailor_id=tailor_id, choice=choice)
        tailor_details= about_tailor_db(tailor_id)
        tailor_address= tailor_details[8]
        tailor_contact= tailor_details[4]
        try:
            temp_orderid = random.randint(a=4400000000, b=4499999999)
            add_temp_order_with_measurements(temp_orderid, customer_id, tailor_id, choice, customer_address, tailor_address, tailor_contact, customer_contact, measurements, order_created, cust_name)
        except:
            taking_order(choice, tailor_id, customer_id)
        finally:
            price= get_price(tailor_id, choice)
            addresses = get_address(customer_id)
            return render_template("order_page.html", temp_orderid=temp_orderid, choice=choice, tailor_id=tailor_id, customer_id=customer_id, cust_details=cust_details[0], tailor_details=tailor_details, price=price, addresses= addresses)
    temp_orderid = temp_oredrid
    price = get_price(tailor_id, choice)
    tailor_details = about_tailor_db(tailor_id)
    addresses = get_address(customer_id)
    cust_details = read_customer_db(customer_id)
    return render_template("order_page.html", temp_orderid=temp_orderid, choice=choice, tailor_id=tailor_id,
                           customer_id=customer_id, cust_details=cust_details[0], tailor_details=tailor_details,
                           price=price, addresses=addresses)

@app.route("/shirt_measurement_guide/<choice>/<tailor_id>/<customer_id>")
def shirt_guide(choice, tailor_id, customer_id):
    return render_template("shirt_measurements_guide.html", choice=choice, tailor_id=tailor_id, customer_id=customer_id)

@app.route("/take_measurements/<garment>/<customer_id>/<tailor_id>/<temp_orderid>", methods=["post", "get"])
def taking_measurements(garment, customer_id, tailor_id, temp_orderid):
    if garment == "shirt":
        return render_template("dimensions_shirt_tailor.html", garment=garment, tailor_id=tailor_id, customer_id=customer_id, temp_orderid=temp_orderid)
    elif garment == "trousers":
        return render_template("dimensions_trouser_tailor.html", garment=garment, tailor_id=tailor_id, customer_id=customer_id, temp_orderid=temp_orderid)
    elif garment == "kurta_men":
        return render_template("dimensions_kurta_men_tailor.html", garment=garment, tailor_id=tailor_id, customer_id=customer_id, temp_orderid=temp_orderid)
    elif garment == "dhoti":
        return render_template("dimensions_dhoti_tailor.html", garment=garment, tailor_id=tailor_id, customer_id=customer_id, temp_orderid=temp_orderid)
    elif garment == "blouse":
        return render_template("dimensions_blouse_tailor.html", garment=garment, tailor_id=tailor_id, customer_id=customer_id, temp_orderid=temp_orderid)
    elif garment == "saree":
        return render_template("dimensions_saree_tailor.html", garment=garment, tailor_id=tailor_id, customer_id=customer_id, temp_orderid=temp_orderid)
    elif garment == "blazer":
        return render_template("dimensions_blazer_tailor.html", garment=garment, tailor_id=tailor_id, customer_id=customer_id, temp_orderid=temp_orderid)
    elif garment == "kurta_women":
        return render_template("dimensions_kurta_women_tailor.html", garment=garment, tailor_id=tailor_id, customer_id=customer_id, temp_orderid=temp_orderid)

@app.route("/update_measurements/<garment>/<tailor_id>/<customer_id>/<temp_orderid>", methods= ["POST", "GET"])
def update_measurements(garment, tailor_id, customer_id, temp_orderid):
    import pdb;pdb.set_trace()
    form_data = request.form
    form_text = "\n".join([f"{key}: {value}" for key, value in form_data.items()])
    update_measurements_in_table(temp_orderid, form_text)
    flash("measurements updated successfully")
    return redirect(url_for("check_login_tailor"))


@app.route("/update_cust_details/<customer_id>/<tailor_id>/<choice>", methods=["GET", "POST"])
def update_cust_address(customer_id, tailor_id, choice):
    customer_address= request.form.get("customer_address")
    customer_email = request.form.get("customer_email")
    update_cust_table(customer_id, customer_address, customer_email)
    return redirect(url_for("taking_order" , customer_id=customer_id, tailor_id=tailor_id, choice=choice ))

@app.route("/payment_page/<customer_id>/<tailor_id>/<choice>/<temp_orderid>", methods=["POST", "GET"])
def payment_page(customer_id, tailor_id, choice, temp_orderid):
    import pdb;pdb.set_trace()
    #price = request.form.get("value")
    price = get_price(tailor_id, choice)
    return render_template("payment_page.html", temp_orderid=temp_orderid, customer_id=customer_id, tailor_id=tailor_id, choice=choice, price=price[0])

@app.route("/pay_now/<choice>/<price>/<customer_id>/<tailor_id>/<temp_orderid>", methods= ["POST", "GET"])
def pay_now_wallet(choice, price, customer_id, tailor_id, temp_orderid):
    cust_details= read_customer_db(customer_id)
    wallet = int(cust_details[0][8])
    if wallet<int(price):
        flash("insufficient funds")
        return redirect(url_for("payment_page", customer_id=customer_id, tailor_id=tailor_id, choice=choice, temp_orderid=temp_orderid))
    update_wallet = wallet - int(price)
    update_cust_wallet(customer_id,update_wallet)
    order_id = random.randint(a=1100000000, b= 1199999999)
    copy_from_unpaid_orders(temp_orderid)
    status_update_unpaid(temp_orderid)
    order_created = datetime.datetime.now()
    create_order(order_id, order_created, temp_orderid)


@app.route("/cust_new_address/<temp_orderid>/<choice>/<customer_id>")
def add_new_address(temp_orderid, choice, customer_id):
    return render_template("add_new_address.html", temp_orderid=temp_orderid, choice=choice, customer_id=customer_id)

@app.route("/add_address_cust/<temp_orderid>/<choice>/<customer_id>", methods= ["POST", "GET"])
def new_address_add(temp_orderid, choice, customer_id):
    name= request.form.get("cust_name")
    address = request.form.get("address")
    contact= request.form.get("contact")
    add_address_to_db(temp_orderid, customer_id, choice, name, address, contact)
    return redirect(url_for("taking_order"))

if __name__ == "__main__":
    app.run(debug=True)