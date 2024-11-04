
import mysql.connector

def order_temp_database():
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    return  my_con


def add_temp_order_with_measurements(temp_orderid, customer_id, tailor_id, choice, customer_address, tailor_address, tailor_contact, customer_contact, measurements, order_created, cust_name):
    my_con = order_temp_database()
    cursor= my_con.cursor()
    query ="""insert into unpaid_orders (temp_orderid, customer_id, tailor_id, choice, customer_address, tailor_address, tailor_contact, customer_contact, measurements, order_created, cust_name) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (temp_orderid, customer_id, tailor_id, choice, customer_address, tailor_address, tailor_contact, customer_contact, measurements, order_created, cust_name))
    my_con.commit()
    my_con.close()

def unpaid_orders_db(tailor_id):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""select * from unpaid_orders where tailor_id = '{tailor_id}' and status = 'waiting' and measurements ='' """
    cursor.execute(query)
    unpaid_orders = cursor.fetchall()
    my_con.close()
    return unpaid_orders

def tailor_orders(tailor_id):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""select * from orders where tailor_id = '{tailor_id}' and (status = 'pending' or status = 'in-progress' )"""
    cursor.execute(query)
    orders = cursor.fetchall()
    my_con.close()
    return orders

def unpaid_orders_customer(customer_id):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""select * from unpaid_orders where customer_id = '{customer_id}' and status = 'waiting' or measurements ='' """
    cursor.execute(query)
    unpaid_orders = cursor.fetchall()
    my_con.close()
    return unpaid_orders

def customer_progress_orders(customer_id):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""select * from orders where customer_id = '{customer_id}' and (status = 'pending' or status = 'in-progress') """
    cursor.execute(query)
    orders = cursor.fetchall()
    my_con.close()
    return orders

def customer_completed_orders(customer_id):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""select * from orders where customer_id = '{customer_id}' and status = 'delivered' """
    cursor.execute(query)
    orders = cursor.fetchall()
    my_con.close()
    return orders


def tailor_paid_orders(tailor_id):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""select * from orders where tailor_id = '{tailor_id}' and status = 'delivered'"""
    cursor.execute(query)
    orders = cursor.fetchall()
    my_con.close()
    return orders


def update_measurements_in_table(temp_orderid, form_text):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""update unpaid_orders set measurements ='{form_text}' where temp_orderid = '{temp_orderid}' """
    cursor.execute(query)
    my_con.commit()
    my_con.close()
    return

def status_update_unpaid(temp_orderid):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""UPDATE unpaid_orders SET status = 'ordered' WHERE measurements IS NOT NULL AND measurements <> '' AND measurements <> 'none' AND temp_orderid = '{temp_orderid}'"""
    cursor.execute(query)
    my_con.commit()
    my_con.close()
    return

def copy_from_unpaid_orders(temp_orderid):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""INSERT INTO orders (temp_orderid, customer_id, tailor_id, choice, customer_address, tailor_address, tailor_contact, customer_contact, measurements) SELECT temp_orderid, customer_id, tailor_id, choice, customer_address, tailor_address, tailor_contact, customer_contact, measurements FROM unpaid_orders where temp_orderid = '{temp_orderid}'"""
    cursor.execute(query)
    my_con.commit()
    my_con.close()
    return



def add_address_to_db(temp_orderid, customer_id, choice, name, address, contact):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = """INSERT INTO address_cust (temp_orderid, customer_id, choice, cust_name, customer_address, customer_contact) values (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (temp_orderid, customer_id, choice, name, address, contact))
    my_con.commit()
    my_con.close()
    return

def get_address(customer_id):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""select * from address_cust where customer_id = '{customer_id}'"""
    cursor.execute(query)
    address = cursor.fetchall()
    my_con.close()
    return address

def create_order(order_id, order_created, temp_orderid):
    my_con = order_temp_database()
    cursor = my_con.cursor()
    query = f"""UPDATE orders SET order_id = '{order_id}', created_on= '{order_created}' WHERE temp_orderid = '{temp_orderid}'"""
    cursor.execute(query)
    my_con.commit()
    my_con.close()
    return
