from flask import *
from auth import *

app= Flask(__name__)
app.secret_key= "147258"


@app.route("/signup",methods= ["GET","POST"])
def user_signup():
    return register()
@app.route("/to_do_list",methods= ["GET","POST"])
def task_page():
    return to_do_list()

@app.route("/" ,methods= ["GET","POST"])
def index():
    return signin()
@app.route("/signin",methods= ["GET","POST"])
def user_signin():
    return validate()

@app.route("/logout_todo")
def log_out():
    return logout()

@app.route("/addtask", methods=["GET","POST"])
def route_addtask():
    return add_task()

@app.route("/edit_todo/<task_id>")
def route_edit_task(task_id):
    return edit_task(task_id)

@app.route("/delete_todo/<task_id>")
def route_delete_task(task_id):
    return delete_task(task_id)

@app.route("/filter_tasks", methods=["get","post"])
def filter_tasks():
    return to_do_list()



if __name__=="__main__":
    app.run(debug=True)