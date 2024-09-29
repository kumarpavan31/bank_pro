import mysql.connector
import random

my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                 database="bank")


# in table(Customers) Name, Username, password, Account_Number, Balance


def usernames():
    for i in range(5):
        my_con1 = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321", database="bank")
        user_name = input("Enter Username: ")

        query1 = f"""select * from  customers where username= '{user_name}'"""
        cursor = my_con1.cursor()
        cursor.execute(query1)
        result = cursor.fetchone()
        if result is not None:
            print("Username already exists")
            continue
        else:
            break
    return user_name



def accountnum():
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
        print(f"your account number is {account_num}")

        return account_num

def name():
    name = input("Enter your Name")
    return name

def password():
    pass_word = input("Enter you password: ")
    if len(pass_word) <= 5:
        print("Minimum five characters required.")
    else:
        return pass_word


def signup():
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321", database="bank")

    try:

        balance = 0


        query = f"""insert into customers values ('{name()}','{usernames()}','{password()}',{accountnum()},{balance})"""


        cursor = my_con.cursor()
        cursor.execute(query)
        my_con.commit()
        print("Your account has been created successfully.")
        opening_menu()
    except Exception as e:
        print(e)
    finally:
        my_con.close()


def signin():
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321", database="bank")
    try:
        user_name = input("Enter Username: ")
        query1 = f"""select * from  customers where username= '{user_name}'"""
        cursor = my_con.cursor()
        cursor.execute(query1)
        result = cursor.fetchone()

    except Exception as e:
        print("Something went wrong", e)
    finally:
        if result is None:
            print("username not found")
            opening_menu()
        else:
            password = input("Enter password:")
            if password == result[2]:
                result1 = list(result)
                print("Login Successful")
                login_menu(result1)
            else:
                print("wrong password entered.")
                opening_menu()
        my_con.close()

def login_menu(result1):
    print("1. Change Password")
    print("2. Check balance")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Fund Transfer")
    print("6. Logout")
    choice = input("Select your choice: ")
    if choice == str(1):
        changepass(result1)
    elif choice == str(2):
        check_bal(result1)
    elif choice == str(3):
        depost(result1)
    elif choice == str(4):
        withdraw(result1)
    elif choice == str(5):
        transfer(result1)
    elif choice == str(6):
        opening_menu()
    else:
        print("Wrong input")
        print("please choose from the options.")
        login_menu(result1)

def changepass(result1):
    old = input("Enter your old password:")
    if old == result1[2]:
        new = input("Enter new password: ")
        my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                         database="bank")
        query = f"""UPDATE customers set password = '{new}' where username ='{result1[1]}'"""
        #result = tuple(result1)
        cursor = my_con.cursor()
        cursor.execute(query)

        my_con.commit()
        my_con.close()
        print("password changed successfully")
    else:
        print("password incorrect")
        login_menu(result1)

def opening_menu():
    print("1. Create Account")
    print("2. Login")
    print("3. Check Balance")
    print("4. Exit")
    x = input("Enter your choice: ")
    if x == str(1):
        signup()
    elif x == str(2):
        signin()
    elif x == str(3):
        pass
    elif x == str(4):
        return
    else:
        print("Wrong input")
        opening_menu()


def check_bal(result1):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="bank")
    query1 = f"""select * from  customers where username = '{result1[1]}'"""
    cursor = my_con.cursor()
    cursor.execute(query1)
    import pdb; pdb.set_trace()
    print(f"your current balance is {result1[4]}")
    login_menu(result1)
    my_con.close()
def depost(result1):
    amount = int(input("Enter amount to deposit: "))
    if amount > 0:
        result1[4] = result1[4] + amount

        query = f"""UPDATE customers set balance = '{result1[4]}' where username ='{result1[1]}'"""
        cursor = my_con.cursor()
        cursor.execute(query)

        my_con.commit()
        my_con.close()
        print("Amount deposited successfully")
        login_menu(result1)
    else:
        print("enter valid amount")
        depost(result1)


def withdraw(result1):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="bank")
    amount = int(input("Enter amount to withdraw: "))
    if amount < 0:
        print("enter a valid amount")
    elif amount<result1[4]:
        result1[4] = result1[4] - amount

        query = f"""UPDATE customers set balance = '{result1[4]}' where username ='{result1[1]}'"""
        cursor = my_con.cursor()
        cursor.execute(query)

        my_con.commit()
        my_con.close()
        print("Amount withdrawn successfully")
        login_menu(result1)
    else:
        print("insufficient funds")
        login_menu(result1)

def transfer(result1):
    my_con = mysql.connector.connect(host="localhost", port=3306, user="root", password="Navap@321",
                                     database="bank")
    for i in range(3):
        accnum = int(input("Enter receivers account number: "))
        query1 = f"""select * from  customers where account_number = '{accnum}'"""
        cursor = my_con.cursor()
        cursor.execute(query1)
        result2 = cursor.fetchone()
        if result2 is None:
            print("Account not found")
            continue
        else:
            result3 = list(result2)
            amount = int(input("Enter amount to transfer: "))
            if amount < 0:
                print("enter a valid amount")
            elif amount < result1[4]:
                result1[4] = result1[4] - amount
                query = f"""UPDATE customers set balance = '{result1[4]}' where username ='{result1[1]}'"""
                cursor = my_con.cursor()
                cursor.execute(query)
                result3[4] = result3[4] + amount
                query1 = f"""UPDATE customers set balance = '{result3[4]}' where account_number ='{accnum}'"""
                cursor = my_con.cursor()
                cursor.execute(query1)

                my_con.commit()
                my_con.close()
                print("Amount transferred successfully")
                break

            else:
                print("insufficient funds")
                login_menu(result1)
    login_menu(result1)

print("Welcome")
x = input("press enter to continue")
if x == str(x):
    opening_menu()

my_con.close()