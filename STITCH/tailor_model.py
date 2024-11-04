import mysql.connector

def register_tailor_db(tailor_id, tailor_name, tailor_email, tailor_contact,tailor_password, experience, tailor_machine, address, gender, revenue, created_on):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    cursor = my_con.cursor()
    query= """INSERT INTO tailor_details (tailor_id, tailor_name, tailor_email, tailor_contact,tailor_password, experience, tailor_machine, address, gender, revenue, created_on) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (tailor_id, tailor_name, tailor_email, tailor_contact,tailor_password, experience, tailor_machine, address, gender, revenue, created_on))
    my_con.commit()
    my_con.close()


def add_tailor_skill(tailor_id, value, shirt, trousers, kurta_men, dhoti, blouse, saree, blazer, kurta_women, minor_stitches, custom, shirt_image, trouser_image, kurta_men_image, dhoti_image, blouse_image, saree_image, blazer_image, kurta_women_image, minor_stitch_image, custom_image):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    cursor = my_con.cursor()
    query = """CALL tailor_skill (%s, %s, %s, %s)"""
    data = [(tailor_id, shirt, value, shirt_image), (tailor_id, trousers, value, trouser_image),
            (tailor_id, kurta_men, value, kurta_men_image), (tailor_id, dhoti, value, dhoti_image), (tailor_id, blouse, value, blouse_image),
            (tailor_id, saree, value, saree_image), (tailor_id, blazer, value, blazer_image),
            (tailor_id, kurta_women, value, kurta_women_image), (tailor_id, minor_stitches, value, minor_stitch_image),
            (tailor_id, custom, value, custom_image)]
    cursor.executemany(query, data)
    my_con.commit()
    my_con.close()


def read_all_skill():
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    query = """SELECT DISTINCT skill_name,image FROM tailor_skill"""
    cursor = my_con.cursor()
    cursor.execute(query)
    skills = cursor.fetchall()
    my_con.close()
    return skills

def read_tailor_skill(tailor_id):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    query = f"""select * from tailor_skill where tailor_id ='{tailor_id}' """
    cursor = my_con.cursor()
    cursor.execute(query)
    skills = cursor.fetchall()
    my_con.close()
    return skills

def set_price_tailor(skill_name, tailor_id, value):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    query = f"""update tailor_skill set value='{value}' where skill_name='{skill_name}' and tailor_id ='{tailor_id}' """
    cursor = my_con.cursor()
    cursor.execute(query)
    my_con.commit()
    my_con.close()
    return


def check_tailor(tailor_contact):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    cursor = my_con.cursor()
    query = f"""select * from tailor_details where tailor_contact = '{tailor_contact}'"""
    cursor.execute(query)
    tailor_details = cursor.fetchone()
    my_con.close()
    return tailor_details


def all_tailor_ids(skill_name):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    cursor = my_con.cursor()
    query = f"""select tailor_id from tailor_skill where skill_name = '{skill_name}'"""
    cursor.execute(query)
    ids = cursor.fetchall()
    my_con.close()
    return ids

def all_tailors_for_skill(ids):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    cursor = my_con.cursor()
    # Constructing a query with multiple IDs
    query = """SELECT * FROM tailor_details WHERE tailor_id IN (%s)""" % ','.join(['%s'] * len(ids))
    cursor.execute(query, ids)
    tailors = cursor.fetchall()
    my_con.close()
    return tailors


def get_tailors_with_skills(skill_name):
    my_con = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Navap@321",
        database="stitch"
    )

    cursor = my_con.cursor()
    query = f"""
    SELECT td.tailor_id, td.tailor_name, ts.skill_name
    FROM tailor_details td
    LEFT JOIN tailor_skill ts ON td.tailor_id = ts.tailor_id
    WHERE skill_name='{skill_name}'
    ORDER BY td.tailor_id;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    my_con.close()
    return results



def about_tailor_skills(tailor_id):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    cursor = my_con.cursor()
    query = f"""select skill_name, value from tailor_skill where tailor_id = '{tailor_id}'"""
    cursor.execute(query)
    skills = cursor.fetchall()
    my_con.close()
    return skills


def about_tailor_db(tailor_id):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    cursor = my_con.cursor()
    query = f"""select * from tailor_details where tailor_id = '{tailor_id}'"""
    cursor.execute(query)
    details = cursor.fetchone()
    my_con.close()
    return details

def get_price(tailor_id, choice):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="stitch")
    cursor = my_con.cursor()
    query = f"""select value from tailor_skill where tailor_id = '{tailor_id}' and skill_name='{choice}'"""
    cursor.execute(query)
    price = cursor.fetchone()
    my_con.close()
    return price