import mysql.connector

class TAILOR:
    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitchtest")

    def add_tailor(self, tailor_id, name, email, contact, password, experience, machine, address, gender, wallet, created_on):
        cursor = self.my_con.cursor()
        query = """insert into tailors (tailor_id, name, email, contact, password, experience, machine, address, gender, wallet, created_on) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (tailor_id, name, email, contact, password, experience, machine, address, gender, wallet, created_on))
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

    def tailor_info(self, tailor_id):
        cursor = self.my_con.cursor()
        query = f"""select * from tailors where tailor_id = '{tailor_id}' """
        cursor.execute(query)
        info = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return info[0]

    def verify_tailor_db(self,contact, password):
        cursor = self.my_con.cursor()
        import pdb;pdb.set_trace()
        query = f"""select tailor_id from tailors where contact = %s and password = %s """
        cursor.execute(query, (contact, password))
        tailor_id = cursor.fetchone()
        cursor.close()
        self.my_con.close()
        return tailor_id[0]


    def check_contact(self):
        cursor = self.my_con.cursor()
        query = f"""select contact from tailors """
        cursor.execute(query)
        contacts = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return contacts


    def change_password(self, tailor_id, contact, password):
        cursor = self.my_con.cursor()
        query = f"""update tailors set password = '{password}' where tailor_id = '{tailor_id}', contact = '{contact}'"""
        cursor.execute(query)
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return




class SKILL:
    def __init__(self):
        self.my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitchtest")


    def add_skills(self, tailor_id, garment, price, image):
        cursor = self.my_con.cursor()
        query = """insert into skills (tailor_id, garment, price, image) values (%s, %s, %s, %s)"""
        cursor.execute(query, (tailor_id, garment, price, image))
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

    def read_skills(self, tailor_id):
        cursor = self.my_con.cursor()
        query = f"""select * from skills where tailor_id = '{tailor_id}' """
        cursor.execute(query)
        skills = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return skills

    def add_price(self, tailor_id, garment, price):
        cursor = self.my_con.cursor()
        query = f"""update skills set price= %s where tailor_id = %s and garment = %s """
        cursor.execute(query, (price, tailor_id, garment))
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return

    def delete_skill(self, tailor_id, garment):
        cursor = self.my_con.cursor()
        query = f"""delete from skills where tailor_id = '{tailor_id}', garment = '{garment}'"""
        cursor.execute(query)
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return


    def price_update(self, tailor_id, garment, price):
        cursor = self.my_con.cursor()
        query = """update skills  (tailor_id, garment, price) values (%s, %s, %s)"""
        cursor.execute(query, (tailor_id, garment, price))
        self.my_con.commit()
        cursor.close()
        self.my_con.close()
        return


    def available_skills(self):
        cursor = self.my_con.cursor()
        query = """select distinct garment, image from skills"""
        cursor.execute(query)
        skills = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return skills

    def available_tailor(self, garment):
        cursor = self.my_con.cursor()
        query = f"""SELECT tailors.tailor_id, tailors.name FROM tailors INNER JOIN skills ON tailors.tailor_id = skills.tailor_id WHERE skills.garment = '{garment}'"""
        cursor.execute(query)
        avail_tailors = cursor.fetchall()
        cursor.close()
        self.my_con.close()
        return avail_tailors

    def get_price(self, tailor_id, garment):
        cursor = self.my_con.cursor()
        query = f"""select price from skills where tailor_id = '{tailor_id}' and garment = '{garment}' """
        cursor.execute(query)
        price = cursor.fetchone()
        cursor.close()
        self.my_con.close()
        return price
