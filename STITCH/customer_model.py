import mysql.connector

def customer_data_database():
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    return  my_con


def add_customer_db(customer_id, customer_name, customer_contact, customer_password, wallet, created_on):
    my_con = customer_data_database()
    cursor = my_con.cursor()
    query = """insert into customer_details(customer_id, customer_name, customer_contact, customer_password, wallet, created_on) values(%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (customer_id, customer_name, customer_contact, customer_password, wallet, created_on))
    my_con.commit()
    my_con.close()

def read_customer_db(customer_id):
    my_con= customer_data_database()
    cursor= my_con.cursor()
    query = f"""select * from customer_details where customer_id = '{customer_id}'"""
    cursor.execute(query)
    cust_details = cursor.fetchall()
    my_con.close()
    return cust_details

def check_customer_db(customer_contact, customer_password):
    my_con= customer_data_database()
    cursor= my_con.cursor()
    query = f"""select * from customer_details where customer_contact = '{customer_contact}' and customer_password = '{customer_password}'"""
    cursor.execute(query)
    cust_data = cursor.fetchone()
    my_con.close()
    return cust_data

def update_customer(customer_id, customer_name, customer_email, address):
    my_con=customer_data_database()
    cursor = my_con.cursor()
    query = f"""update customer_details set customer_name='{customer_name}' , customer_email='{customer_email}', address='{address}' where customer_id = '{customer_id}'"""
    cursor.execute(query)
    my_con.commit()
    my_con.close()
    return

def add_money_to_wallet(customer_id, wallet):
    my_con = customer_data_database()
    cursor = my_con.cursor()
    query = f"""update customer_details set wallet='{wallet}' where customer_id = '{customer_id}'"""
    cursor.execute(query)
    my_con.commit()
    my_con.close()
    return

def update_cust_table(customer_id, customer_address, customer_email):
    my_con = customer_data_database()
    cursor = my_con.cursor()
    query = f"""update customer_details set address='{customer_address}' , customer_email='{customer_email}' where customer_id = '{customer_id}'"""
    cursor.execute(query)
    my_con.commit()
    my_con.close()
    return


def update_cust_wallet(customer_id,update_wallet):
    my_con = customer_data_database()
    cursor = my_con.cursor()
    query = f"""update customer_details set wallet='{update_wallet}' where customer_id = '{customer_id}'"""
    cursor.execute(query)
    my_con.commit()
    my_con.close()
    return

#class MyConnection():

#    def __init__(MyConnect):
#        MyConnect.con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
#                                     database="stitch")
#    def insert_customer(MyConnect):
#        MyConnect.update_customer()
#    def update_customer(MyConnect):
#        my_con = MyConnect.con

 #   self.update_customer()

#update_customer()

#MyConnection.update_customer()

#obj= MyConnection()

#obj.update_customer()
