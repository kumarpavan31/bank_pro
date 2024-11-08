import mysql.connector




class DELIVERY_PARTNER:

    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitchtest")

    def verify_login(self, contact, password):
        cursor = self.my_con.cursor()
        query = f"""select executive_id from executives where contact = '{contact}' and password = '{password}'"""
        cursor.execute(query)
        executive_id = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return executive_id


    def add_executive(self, executive_id, name, email, contact, password, address, created_on):
        cursor = self.my_con.cursor()
        query = """insert into tailors (executive_id, name, email, contact, password, address, created_on) values (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (
        executive_id, name, email, contact, password, address, created_on))
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

    def check_contact(self):
        cursor = self.my_con.cursor()
        query = f"""select contact from executives """
        cursor.execute(query)
        contacts = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return contacts