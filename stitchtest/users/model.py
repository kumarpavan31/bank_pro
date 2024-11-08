import mysql.connector

class USERS:
    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitchtest")

    def add_customer(self, user_id, name, contact, password, created_on):
        cursor = self.my_con.cursor()
        query = """insert into customers (user_id, name, contact, password, created_on) values (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (user_id, name, contact, password, created_on))
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return


    def change_password(self, user_id, password):
            cursor = self.my_con.cursor()
            query = f"""update customers set password = '{password}' where user_id = '{user_id}'"""
            cursor.execute(query)
            self.my_con.commit()
            cursor.close()
            self.my_con.close()
            return

    def verify_login(self, contact, password):
        cursor = self.my_con.cursor()
        query = f"""select user_id from customers where contact = '{contact}' and password = '{password}'"""
        cursor.execute(query)
        user_id = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return user_id

    def user_info(self, user_id):
        cursor = self.my_con.cursor()
        query = f"""select * from customers where user_id = '{user_id}'"""
        cursor.execute(query)
        user = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return user

    def check_contact(self):
        cursor = self.my_con.cursor()
        query = f"""select contact from customers """
        cursor.execute(query)
        contacts = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return contacts


class ADDRESS:
    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitchtest")

    def add_address(self, user_id, name, email, contact, address):
        cursor = self.my_con.cursor()
        query = """insert into address (user_id, name, email, contact, address) values (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (user_id, name, email, contact, address))
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

    def del_address(self, user_id, address):
        cursor = self.my_con.cursor()
        query = f"""delete from address where user_id = '{user_id}' and address='{address}'"""
        cursor.execute(query)
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return


    def get_all_address(self, user_id):
        cursor = self.my_con.cursor()
        query = f"""select * from address where user_id = '{user_id}'"""
        cursor.execute(query)
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return


class MEASUREMENTS:

    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                              database="stitchtest")

    def add_measurements(self, user_id, garment, measurements ):
        cursor = self.my_con.cursor()
        query = """insert into address (user_id, garment, measurements) values (%s, %s, %s)"""
        cursor.execute(query, (user_id, garment, measurements))
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

