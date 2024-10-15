import mysql.connector
from auth import *

def adduser(name, usermail, password):
    mycon,cursor = get_db_connection()
    query = f"""insert into users( user_name, user_mail, user_password)  values('{name}','{usermail}','{password}')"""
    #cursor = mycon.cursor()
    cursor.execute(query)
    mycon.commit()
    mycon.close()
    return


def get_user_details(username):
    mycon,cursor = get_db_connection()
    query = f"""select * from users where user_name='{username}'"""
    #cursor = mycon.cursor()
    cursor.execute(query)
    user_details = cursor.fetchone()
    mycon.close()
    return user_details

def get_user_tasks(user_name):
    mycon,cursor = get_db_connection()
    query = f"""select * from todo_list where user_name = '{user_name}'"""
    #cursor = mycon.cursor()
    cursor.execute(query)
    task_list = cursor.fetchall()
    mycon.close()
    return task_list

def get_task_count(user_name):
    mycon,cursor = get_db_connection()
    query = f"""SELECT COUNT(user_name) AS Number_of_tasks FROM todo_list where user_name = '{user_name}'"""
    #cursor = mycon.cursor()
    cursor.execute(query)
    count = cursor.fetchone()
    mycon.close()
    return count[0]

def insert_task(user_name, task_name, task_date, completion_time, task_status, priority, created_on):
    mycon,cursor = get_db_connection()
    query = f"""insert into todo_list( user_name, task_name, task_date, completion_time, task_status, priority, created_on) values('{user_name}','{task_name}','{task_date}','{completion_time}','{task_status}','{priority}','{created_on}')"""
    #cursor = mycon.cursor()
    cursor.execute(query)
    mycon.commit()
    mycon.close()
    return

def checkuser(username):
    mycon,cursor = get_db_connection()
    query = f"""select * from users where user_name='{username}'"""
    #cursor = mycon.cursor()
    cursor.execute(query)
    user_details = cursor.fetchone()
    mycon.close()
    return user_details

def edit_task_db(task_name,priority,task_status,task_id):
    mycon,cursor = get_db_connection()
    query = f"""UPDATE todo_list set task_name='{task_name}', priority='{priority}', task_status='{task_status}' where created_on='{task_id}'"""
    #cursor = mycon.cursor()
    cursor.execute(query)
    mycon.commit()
    mycon.close()
    return

def delete_task_db(task_id):
    mycon,cursor = get_db_connection()
    query = f"""delete from todo_list where created_on='{task_id}'"""
    #cursor = mycon.cursor()
    cursor.execute(query)
    mycon.commit()
    mycon.close()
    return

def get_db_connection():
    mycon = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                    database="todo_M")
    cursor = mycon.cursor()

    return mycon, cursor

def sort_tasks(priority, task_status):
    mycon,cursor= get_db_connection()
    if priority and task_status:
        query= f"""select * from todo_list where task_status='{task_status}' and priority='{priority}'"""
    elif priority:
        query = f"""select * from todo_list where priority='{priority}'"""
    elif task_status:
        query = f"""select * from todo_list where task_status='{task_status}'"""
    cursor.execute(query)
    filtered_tasks= cursor.fetchall()
    mycon.close()
    return filtered_tasks


def db_connection(func):
    def wrapper(*args, **kwargs):
        mycon = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                        database="todo_M")
        cursor = mycon.cursor()

        try:
            query = func(*args, **kwargs)
            cursor.execute(query)
            result = cursor.fetchall()

            return result
        finally:
            mycon.close()

    return wrapper

@db_connection
def sort_tasks1(priority, task_status):
    if priority and task_status:
        query= f"""select * from todo_list where task_status='{task_status}' and priority='{priority}'"""
    elif priority:
        query = f"""select * from todo_list where priority='{priority}'"""
    elif task_status:
        query = f"""select * from todo_list where task_status='{task_status}'"""
    return query