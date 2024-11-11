import mysql.connector



class ORDERS:
    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitchtest")

    def add_order(self, order_id, user_id, tailor_id, customer_address, customer_name, customer_contact, tailor_address, tailor_contact, tailor_name, garment, price, ordered_on):
        cursor = self.my_con.cursor()
        query = """insert into orders (order_id, user_id, tailor_id, customer_address, customer_name, customer_contact, tailor_address, tailor_contact, tailor_name, garment, value, ordered_on) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (order_id, user_id, tailor_id, customer_address, customer_name, customer_contact, tailor_address, tailor_contact, tailor_name, garment, price, ordered_on))
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

    def update_status_waiting(self, order_id, otp, executive_id, executive_contact, executive_name):
        cursor = self.my_con.cursor()
        query = f"""update orders set status = 'Waiting', customer_otp = '{otp}', executive_contact='{executive_contact}', executive_id= '{executive_id}', executive_name= '{executive_name}' where order_id = '{order_id}'"""
        cursor.execute(query)
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

    def define_order(self, order_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where order_id = '{order_id}'"""
        cursor.execute(query)
        order_info = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return order_info

    def update_measurements(self, order_id, measurements, otp):
        cursor = self.my_con.cursor()
        query = f"""update orders set measurements = '{measurements}', status = 'Pending', tailor_otp='{otp}' where order_id = '{order_id}'"""
        cursor.execute(query)
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

    def update_status_inprogress(self, order_id):
        cursor = self.my_con.cursor()
        query = f"""update orders set status = 'In Progress' where order_id = '{order_id}'"""
        cursor.execute(query)
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

    def cancel_the_order(self, order_id, reason):
        cursor = self.my_con.cursor()
        query = f"""update orders set status = 'Cancelled', remarks ='{reason}' where order_id = '{order_id}'"""
        cursor.execute(query)
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return


class CUSTOMER_ORDERS:

    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitchtest")


    def waiting_orders(self, user_id):
        cursor = self.my_con.cursor()
        query = f"""SELECT * FROM orders WHERE status IN ('Pending', 'Waiting', 'In Progress') or status is null and user_id = '{user_id}'"""
        cursor.execute(query)
        waiting_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return waiting_orders

    def in_transit_orders(self, user_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where status ='Completed' and user_id = '{user_id}'"""
        cursor.execute(query)
        in_transit_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return in_transit_orders


    def delivered_orders(self, user_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where status ='Delivered' and user_id = '{user_id}'"""
        cursor.execute(query)
        delivered_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return delivered_orders




class EXECUTIVE_ORDERS:

    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                              database="stitchtest")

    def waiting_orders(self):
        cursor = self.my_con.cursor()
        query = """select * from orders where status = 'ordered'"""
        cursor.execute(query)
        waiting_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return waiting_orders

    def working_orders(self, executive_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where status ='Waiting' and executive_id = '{executive_id}'"""
        cursor.execute(query)
        working_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return working_orders


    def to_deliver_to_tailor(self, executive_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where status ='Pending' and executive_id = '{executive_id}'"""
        cursor.execute(query)
        pending_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return pending_orders


    def to_deliver_orders(self, executive_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where status ='Completed' and executive_id = '{executive_id}'"""
        cursor.execute(query)
        to_deliver_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return to_deliver_orders


class TAILOR_ORDERS:

    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                              database="stitchtest")


    def booking_orders(self, tailor_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where status is null and tailor_id = '{tailor_id}'"""
        cursor.execute(query)
        waiting_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return waiting_orders

    def waiting_orders(self, tailor_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where status IN ('ordered' , 'Pending' , 'Waiting') and tailor_id = '{tailor_id}'"""
        cursor.execute(query)
        waiting_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return waiting_orders


    def working_orders(self, tailor_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where status ='In Progress' and tailor_id = '{tailor_id}'"""
        cursor.execute(query)
        working_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return working_orders


    def completed_orders(self, tailor_id):
        cursor = self.my_con.cursor()
        query = f"""select * from orders where status ='Completed' or status = 'Delivered' and tailor_id = '{tailor_id}'"""
        cursor.execute(query)
        completed_orders = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return completed_orders
