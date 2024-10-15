from flask import *
import datetime
from model import *

def to_do_list():
    user_name= session.get("user_name")
    priority = request.form.get("filter_priority")
    task_status = request.form.get("filter_status")
    task_list= get_user_tasks(user_name)
    task_count= get_task_count(user_name)
    if priority or task_status:
        task_list = sort_tasks1(priority, task_status)
        task_count= len(task_list)
    return render_template("todo_M.html", tasks=task_list, count=task_count, name=user_name)


def add_task():
    user_name = session.get("user_name")
    task_name = request.form["task_name"]
    task_date = request.form["task_date"]
    completion_time = request.form["completion_time"]
    task_status = request.form["task_status"]
    priority = request.form["priority"]
    created_on = datetime.datetime.now()
    insert_task(user_name, task_name, task_date, completion_time, task_status, priority, created_on)
    return redirect(url_for("task_page"))

def edit_task(task_id):
    task_name = request.args["task_name"]
    priority = request.args["priority"]
    task_status = request.args["task_status"]
    edit_task_db(task_name,priority,task_status,task_id)
    return redirect(url_for("task_page"))

def delete_task(task_id):
    delete_task_db(task_id)
    return redirect(url_for("task_page"))
