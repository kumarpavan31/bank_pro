from flask import *
import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key= "147258"



@app.route("/addtask", methods=["POST"])
def add_to_do():
    task_name = request.form["task_name"]
    task_date = request.form["task_date"]
    completion_time = request.form["completion_time"]
    task_status = request.form["task_status"]
    priority = request.form["priority"]
    created_on = datetime.datetime.now()
    mycon = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                          database="to_do")
    query = f"""insert into todo_list( task_name, task_date, completion_time, task_status, priority, created_on) values('{task_name}','{task_date}','{completion_time}','{task_status}','{priority}','{created_on}')"""
    cursor = mycon.cursor()
    cursor.execute(query)
    mycon.commit()
    mycon.close()
    flash("task is saved successfully")
    return redirect(url_for("to_do_list"))


@app.route("/")
def to_do_list():

    mycon = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                    database="to_do")
    query= """select * from todo_list"""
    cursor= mycon.cursor()
    cursor.execute(query)
    task_list = cursor.fetchall()
    mycon.close()
    #import pdb; pdb.set_trace()
    print(task_list)
    return render_template("todo.html", tasks=task_list)


@app.route("/delete_todo/<task_id>")
def delete_task(task_id):
    mycon = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                    database="to_do")
    query= f"""delete from todo_list where task_id='{task_id}'"""
    cursor = mycon.cursor()
    cursor.execute(query)
    mycon.commit()
    mycon.close()
    flash("task deleted successfully")
    return redirect(url_for("to_do_list"))

@app.route("/edit_todo/<task_id>")
def edit_todo(task_id):
    mycon = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                    database="to_do")
    task_name= request.args["task_name"]
    priority=request.args["priority"]
    task_status = request.args["task_status"]
    query = f"""UPDATE todo_list set task_name='{task_name}', priority='{priority}', task_status='{task_status}' where task_id='{task_id}'"""
    cursor = mycon.cursor()
    cursor.execute(query)
    mycon.commit()
    mycon.close()
    return redirect(url_for("to_do_list"))
@app.route("/register")
def register_page():
    return render_template("register.html")
@app.route("/a")
def welcome():
    return render_template("Welcome.html")
@app.route("/signin")
def signin_page():
    return render_template("signin.html")

def register():
    name= request.form["name"]
    username= request.form["username"]
    password= request.form["password"]



if __name__ == "__main__":
    app.run(debug=True)