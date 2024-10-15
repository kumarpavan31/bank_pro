from flask import *
from model import *
from task import *


def signup():
    return render_template("sign_up_page.html")

def register():
    if request.method=="GET":
        return render_template("sign_up_page.html")
    username=request.form["username"]
    #check_user = checkuser(username)
    #if check_user is not None:
        #return jsonify("user already exists")
    email= request.form["email"]
    password= request.form["password"]
    adduser(username, email, password)
    return render_template("sign_in_page.html")


def signin():
    return render_template("sign_in_page.html")

def validate():
    if request.method=="GET":
        return render_template("sign_in_page.html")
    #if session.get("user_name") and request.method== "GET":
        #return render_template("sign_in_page.html", error="invalid Credentials")
    username= request.form["username"]
    password = request.form["password"]
    user_details = get_user_details(username)
    if user_details and user_details[3] == password:
        session["user_name"]= username
        return redirect(url_for("task_page"))
    return render_template("sign_in_page.html", error= "invalid Credentials")


def logout():
    session.pop("user_name")
    #flash("logged out successfully")
    return redirect(url_for("index"))