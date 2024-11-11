from flask import Flask, blueprints, render_template, redirect, url_for, session
from orders.orders import orders
from tailor.tailor import tailor
from tailor.model import SKILL
from users.users import users
from executive.executive import executive
import base64


app = Flask(__name__)
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(tailor, url_prefix="/tailor")
app.register_blueprint(orders, url_prefix="/orders")
app.register_blueprint(executive, url_prefix="/executive")
app.config["SECRET_KEY"] = "pakodi"

def b64encode(data):
    return base64.b64encode(data).decode('utf-8')
app.jinja_env.filters['b64encode'] = b64encode

@app.route("/")
def opening_page():
    services = SKILL().available_skills()
    return render_template("opening_page.html", services=services)


@app.route("/available_tailors/<garment>", methods= ["post", "get"])
def available_tailors(garment):
    available_tailors = SKILL().available_tailor(garment)
    return render_template("available_tailors.html", available_tailors=available_tailors, garment=garment)


@app.route("/selected_tailor/<garment>/<tailor_id>/<tailor_name>")
def about_tailor(tailor_id, garment, tailor_name):
    tailor_skills = SKILL().read_skills(tailor_id)
    return render_template("about_tailor.html", tailor_id=tailor_id, tailor_skills=tailor_skills, garment=garment, tailor_name=tailor_name)


if __name__ == "__main__":
    app.run(debug=True)