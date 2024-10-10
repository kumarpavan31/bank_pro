from flask import *
import random
import mysql.connector

app = Flask(__name__)
app.secret_key='pakodi'

@app.route('/')
def welcome():
    return render_template("Welcome.html")
    #request.form["submit"]

@app.route('/opening_menu', methods = ["GET","POST"])
def openingmenu():
    return render_template("opening_menu.html")


@app.route('/signup', methods = ["POST"])
def signup():
    return render_template("signup.html")


@app.route('/registered', methods=["POST"])
def registerd():
    def given_user():
        user_id = request.form["username"]
        try:
            my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                             database="bank")
            query1 = f"""select * from  customers where username= '{user_id}'"""
            cursor = my_con.cursor()
            cursor.execute(query1)
            result = cursor.fetchone()
            my_con.close()
            if result is not None:
                return render_template("signup.html", error="Username already exists")
            else:
                return user_id
        except Exception as e:
            return render_template("signup.html", error=e)
    def create_accountnum():
        for i in range(8):
            my_con1 = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                              database="bank")
            account_num = random.randint(90000000, 99999999)
            query = f"""select * from  customers where account_number= '{account_num}'"""
            cursor = my_con1.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            if result is not None:
                continue
            else:
                break

        return account_num


    cust_name = request.form["name"]
    user_id = given_user()
    pass_word = request.form["password"]
    try:
        accountnum = create_accountnum()
        balance = 0

        my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                             database="bank")
        #import pdb; pdb.set_trace()
        query = f"""insert into customers values ('{cust_name}','{user_id}','{pass_word}',{accountnum},{balance})"""

        cursor = my_con.cursor()
        cursor.execute(query)
        my_con.commit()
        my_con.close()

        return render_template("registered.html", account_num=accountnum)

    except Exception as e:
        return render_template("signup.html", error=e)








@app.route('/login', methods = ["GET", "POST"])
def login():
    return render_template("login.html")



@app.route("/dashboard", methods= ["get","post"])
def checklogin():
    #import pdb; pdb.set_trace()
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                      database="bank")
    if request.method == "GET":
        data = session.get('form_data', {}).get('username')
        query1 = f"""select * from  customers where username= '{data}'"""
        cursor = my_con.cursor()
        cursor.execute(query1)
        result = cursor.fetchone()
        result2 = list(result)
        name= result2[0]
        #if result1[4]<result2[4]:
        return render_template("dashboard.html", name=name)
        #else:
            #return render_template("dashboard.html", name=name)
    else:
        try:
            user_name = request.form["username"]
            #user_name = input("Enter Username: ")
            query1 = f"""select * from  customers where username= '{user_name}'"""
            cursor = my_con.cursor()
            cursor.execute(query1)
            result = cursor.fetchone()

        except Exception as e:
            data = session.get('form_data', {}).get('username')
        finally:
            if result is None:
                return render_template("login.html", error="Username Not Found")
            else:
                password = request.form["password"]

                if password == result[2]:
                    global result1
                    result1 = list(result)
                    name= result1[0]
                    username= result1[1]
                    password= result1[2]
                    account_num= result1[3]
                    balance= result1[4]
                    session['form_data']= request.form
                    return render_template("dashboard.html", name=name, username=username, password=password, account_num=account_num, balance=balance)

                    #login_menu(result1)
                else:
                    return render_template("login.html", error= "incorrect password")
                    #opening_menu()
            my_con.close()

@app.route('/check_bal')
def check_bal():
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                      database="bank")
    data = session.get('form_data', {}).get('username')
    query1 = f"""select * from  customers where username= '{data}'"""
    cursor = my_con.cursor()
    cursor.execute(query1)
    result = cursor.fetchone()
    result2 = list(result)
    balance = result2[4]
    my_con.close()
    bal = f"Your current balance is {balance}"
    return render_template("check_bal.html", balance=bal)

@app.route("/deposit", methods= ["GET","POST"])
def deposit():
    data = session.get('form_data',{}).get('username')
    return render_template("deposit.html", form_data=data)


@app.route("/depositdone", methods= ["get", "post"])
def depositmoney():
    #import pdb; pdb.set_trace()
    depositmoney = int(request.form["amount"])
    #balance = int(request.form['balance'])
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                      database="bank")
    data = session.get('form_data', {}).get('username')
    query1 = f"""select * from  customers where username= '{data}'"""
    cursor = my_con.cursor()
    cursor.execute(query1)
    result = cursor.fetchone()
    result2= list(result)
    if depositmoney > 0:
        result2[4] = result2[4] + depositmoney

        query = f"""UPDATE customers set balance = '{result2[4]}' where username ='{result2[1]}'"""
        cursor = my_con.cursor()
        cursor.execute(query)

        my_con.commit()
        my_con.close()
        return render_template("message.html", show="Amount deposited successfully")

    else:
        return render_template("deposit.html", wrong="Enter Valid Amount" )
@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template("logout.html")

@app.route("/withdraw", methods= ["GET", "POST"])
def withdraw():
    #import pdb; pdb.set_trace()
    data = session.get('form_data',{}).get('username')
    return render_template("withdraw.html", form_data=data)

@app.route("/withdrawdone", methods= ["GET", "POST"])
def withdrawmoney():
    #import pdb; pdb.set_trace()
    withdrawmoney = int(request.form["amount"])
    #withdrawmoney = int(request.form["amount"])
    #balance = int(request.form['balance'])
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                      database="bank")
    data = session.get('form_data', {}).get('username')
    query1 = f"""select * from  customers where username= '{data}'"""
    cursor = my_con.cursor()
    cursor.execute(query1)
    result = cursor.fetchone()
    result2= list(result)
    if withdrawmoney > result2[4]:
        return render_template("withdraw.html", wrong="Insufficient funds")
    else:
        result2[4] = result2[4] - withdrawmoney

        query = f"""UPDATE customers set balance = '{result2[4]}' where username ='{result2[1]}'"""
        cursor = my_con.cursor()
        cursor.execute(query)

        my_con.commit()
        my_con.close()
        return render_template("message.html", show="Amount withdrawn successfully")
@app.route("/fundtransfer", methods= ["POST"])
def fundtransfer():
    return render_template("fundtransfer.html")
@app.route("/transferred", methods= ["GET", "POST"])
def transferred():
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="bank")
    data = session.get('form_data', {}).get('username')
    query1 = f"""select * from  customers where username= '{data}'"""
    cursor = my_con.cursor()
    cursor.execute(query1)
    result = cursor.fetchone()
    result2 = list(result)

    to_account= request.form["to_account"]
    to_amount = int(request.form["to_amount"])
    query1 = f"""select * from  customers where account_number= '{to_account}'"""
    cursor = my_con.cursor()
    cursor.execute(query1)
    toresult = cursor.fetchone()
    if toresult is None:
        return render_template("fundtransfer.html", msg="Account not found")
    else:
        if result2[4]<to_amount:
            return render_template("fundtransfer.html", msg="Insufficient Funds")
        elif to_amount<=0:
            return render_template("fundtransfer.html", msg="Enter valid amount")
        else:
            toresult1 = list(toresult)
            result2[4] = result2[4] - to_amount
            toresult1[4] = toresult1[4] + to_amount
            query = f"""UPDATE customers set balance = '{result2[4]}' where username ='{result2[1]}'"""
            query1 = f"""UPDATE customers set balance = '{toresult1[4]}' where username ='{toresult1[1]}'"""
            cursor = my_con.cursor()
            cursor.execute(query)
            cursor.execute(query1)
            my_con.commit()
            my_con.close()
            return render_template("message.html", show= "Amount transferred successfully")

@app.route("/changepassword", methods=["POST"])
def changepassword():
    return render_template("changepassword.html")


@app.route("/changedpassword", methods=["POST"])
def change_password():
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="bank")
    data = session.get('form_data', {}).get('username')
    query1 = f"""select * from  customers where username= '{data}'"""
    cursor = my_con.cursor()
    cursor.execute(query1)
    result = cursor.fetchone()
    result2 = list(result)
    oldpwd= request.form["old"]
    newpswd= request.form["new"]
    confirmnew = request.form['newpwd']
    if oldpwd != result2[2]:
        return render_template("changepassword.html", wrong="Enter correct password")
    else:
        if newpswd != confirmnew:
            return render_template("changepassword.html", wrong="password mismatch")
        else:

            query2 = f"""UPDATE customers set password = '{newpswd}' where username ='{result2[1]}'"""
            cursor = my_con.cursor()
            cursor.execute(query2)
            my_con.commit()
            my_con.close()
            return render_template("changedpassword.html")



if __name__ == '__main__':
    app.run(debug=True)
