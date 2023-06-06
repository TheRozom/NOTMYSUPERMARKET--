import re
from flask import render_template, flash, redirect, url_for
from flask import session, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for
import pandas
from item import Item
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session
from flask import session, make_response
from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
import pandas as pd
import schedule
import time
import subprocess
import threading


app = Flask(__name__)

df = pandas.read_excel("shufersal.xlsx")
DATABASE = "database.db"
app.secret_key = "123456"
x1 = 0
shopping_cart_names = set({})
# subprocess.run(["python", "quickbout.py"])
# subprocess.run(["python", "shupersalbot.py"])


def run1():
    while True:
        try:
            subprocess.run(["python", "quickbout.py"])
            time.sleep(43200)  # 12 hours
        except:
            thread.exit()


def run2():
    while True:
        try:
            subprocess.run(["python", "shupersalbot.py"])
            time.sleep(43200)  # 12 hours
        except:
            thread2.exit()


thread = threading.Thread(target=run1)
thread.start()
thread2 = threading.Thread(target=run2)
thread2.start()


def name_to_cart():
    shopping_cart = []

    for item in shopping_cart_names:
        name, grams = item
        print(name)
        print(grams)

        try:
            item_data = df[df.NAME == name][df.GRAM == grams].iloc[0].tolist()
        except:
            item_data = (
                df[df.NAME == name][df.GRAM.str.contains(grams)].iloc[0].tolist()
            )
        item = Item(*item_data[1:])
        shopping_cart.append(item)

    return shopping_cart


# def name_to_cart():
#     shopping_cart = []

#     for item in session.get('cart', []):
#         name, grams = item
#         item_data = df[df.NAME == name][df.GRAM == grams].iloc[0].tolist()
#         item = Item(*item_data[1:])
#         shopping_cart.append(item)

#     return shopping_cart
# print("\n\n\n\n")
# shopping_cart = []
# print(f"NAMES= {shopping_cart_names}")

# for items in shopping_cart_names:

#     try:
#         name, grams = items
#         print(name)
#         item = df[df.NAME == name][df.GRAM == grams].iloc[0].tolist()

#         print(f"ITEM= {item} \n\n\n")

#         name = item[1]
#         price = item[2]
#         gram = item[3]
#         image_link = item[4]

#         item = Item(name, price, gram, image_link)
#         shopping_cart.append(item)
#     except:
#         print("\n\n")
# return shopping_cart


@app.route("/")
def main_page():
    # if (session['logged_in'] != True):
    # session['logged_in'] = False
    df = pandas.read_excel("shufersal.xlsx")
    return render_template("index.html", df=df)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/cart")
def cart():
    cart = name_to_cart()
    price = 0
    priceq = 0
    df2 = pandas.read_excel("quik.xlsx")
    num2 = 0
    for item in cart:
        # print(df[df.eq(item.name).any(1)] )
        # print("?????????????")
        gramnumber = ""
        for char in item.gram:
            if char.isdigit():
                gramnumber += char
            else:
                break
        print(gramnumber)
        price = price + item.price
        # try:
        #     print(gramnumber)
        #     num2 = df[df.GRAM == int(gramnumber)].iloc[0].tolist()[3]
        #     # num2 = df.loc[(df['NAME'].__contains__(item.name)) &
        #     #               (df['GRAM'] == gramnumber)].iloc[0]['PRICE']
        #     print(num2)
        #     item.price2 = num2
        # except:
        #     pass

        num2 = item.price2
        priceq = priceq + num2

    price = round(price, 2)
    priceq = round(priceq, 2)
    return render_template("cart.html", shopping_cart=cart, price=price, priceq=priceq)


# @app.route('/remove_from_cart')
# def remove_from_cart():
#     item_name = request.args.get("item_name")
#     grams = request.args.get('grams')

#     cart = session.get('cart', [])
#     cart.remove((item_name, grams))
#     session['cart'] = cart

#     return redirect(url_for('cart'))

# @app.route('/add_to_cart', methods=["GET", "POST"])
# def add_to_cart():
#     item_name = request.args.get("item_name")
#     grams = request.args.get('grams')
#     shopping_cart_names.add((item_name, grams))
#     return redirect(url_for('cart'))


# @app.route('/add_to_cart')
# def add_to_cart():
#     item_name = request.args.get("item_name")
#     grams = request.args.get('grams')

#     cart = session.get('cart', [])
#     cart.append((item_name, grams))
#     session['cart'] = cart

#     return redirect(url_for('cart'))


@app.route("/add_to_cart", methods=["GET", "POST"])
def add_to_cart():
    item_name = request.args.get("item_name")
    grams = request.args.get("grams")
    shopping_cart_names.add((item_name, grams))

    return redirect(url_for("cart"))


@app.route("/remove_from_cart", methods=["GET", "POST"])
def remove_from_cart():
    item = request.args.get("item")
    print("<><")
    print(shopping_cart_names)
    item = item.replace(" מוצר זה אינו זמין בסופר " + "quick", "")
    item = re.sub(r"\s*\(.*?\)\s*", "", item)
    grams = request.args.get("grams")
    i = 5
    try:
        shopping_cart_names.remove((item, grams))
    except:
        return redirect(url_for("cart"))

    return redirect(url_for("cart"))


# @app.route('/remove_from_cart')
# def remove_from_cart():
#     item_name = request.args.get("item_name")
#     grams = request.args.get('grams')

#     cart = session.get('cart', [])

#     if (item_name, grams) in cart:
#         cart.remove((item_name, grams))
#         session['cart'] = cart

#     return redirect(url_for('cart'))

# @app.route('/remove_from_cart', methods=["GET", "POST"])
# def remove_from_cart():
#     item_name = request.args.get("item_name")
#     grams = request.args.get('grams')

#     if (item_name, grams) in shopping_cart_names:
#         shopping_cart_names.remove((item_name, grams))
#         flash(f"{item_name} {grams} has been removed from your cart", 'success')
#     else:
#         flash("Item not found in cart", 'danger')

#     return redirect(url_for('cart'))


# @app.route('/search', methods=["GET", "POST"])
# def search_results():

#     query = request.args.get('query')
#     # print(query)
#     if isinstance(query, str):
#         results = df[df['NAME'].str.contains(query, case=False)]
#         # print(results)
#         names = results.loc[:, 'NAME'].values
#         # print(names)
#         # print("W")
#     else:
#         # print("L")
#         return render_template("index.html", df=df, results=results)
#     if (results.empty):
#         # print("no products match your search")
#         return render_template("no_results.html", df=df)
#     try:
#         results['GRAM'] = results['GRAM'].str.extract('(\d+)').astype(int)
#     except:
#         pass
#     return render_template('search_results.html', results=results, df=df)

#     # return render_template('search_results.html', results=results)
#     # return render_template("index.html", df=df)
# # Call the function to create the table when the app starts
# # # Define a function to create the table in the database
# @app.route('/search', methods=["GET", "POST"])
# def search_results():


#     query = request.args.get('query')
#     print(query)
#     if isinstance(query, str):
#         results = df[df['NAME'].str.contains(query, case=False)]
#         print(results)
#         names = results.loc[:, 'NAME'].values
#         print(names)
#         print("W")
#     else:
#         print("L")
#         return render_template("index.html", df=df, results=results)
#     if (results.empty):
#         print("no products match your search")
#         return render_template("no_results.html", df=df)
#     try:
#         results['GRAM'] = results['GRAM'].str.extract('(\d+)').astype(int)
#     except:
#         pass
#     return render_template('search_results.html', results=results, df=df)
@app.route("/search", methods=["GET", "POST"])
def search_results():
    query = request.args.get("query")
    query = re.sub(r"[^א-ת\s\w]+", "", query)
    print(query)
    if isinstance(query, str):
        results = df[df["NAME"].str.contains(query, case=False)]
        print(results)
        names = results.loc[:, "NAME"].values
        print(names)
        print("W")
    else:
        print("L")
        return render_template("index.html", df=df, results=results)
    if results.empty:
        print("no products match your search")
        return render_template("no_results.html", df=df)

    return render_template("search_results.html", results=results, df=df, query=query)


def create_table():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT)""")
    conn.commit()
    conn.close()


create_table()


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("main_page"))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         # Check if the email and password are correct
#         conn = sqlite3.connect(DATABASE)
#         cur = conn.cursor()
#         password = (str(password))
#         password = hashlib.sha1(password.encode()).hexdigest()
#         cur.execute(
#             "SELECT * FROM users WHERE email=? AND password=?", (email, password))
#         user = cur.fetchone()
#         conn.close()

#         # Redirect the user to the main page
#         if not user:
#             # Display an error message
#             error_msg = "Incorrect email or password"
#             return render_template("login.html", error_msg=error_msg)
#             # session['logged_in'] = True
#             # session['current_user'] = {'email': email}
#             # session['logged_in'] = True
#             # return redirect(url_for('main_page'))
#         session['logged_in'] = True
#         return redirect(url_for('main_page'))

#     return render_template("login.html")

# # @app.route('/register', methods=["GET", "POST"])
# # # def register():
# #     return render_template("register.html")


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     session['logged_in'] = False
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password1']
#         password_confirm = request.form['password2']

#         if password != password_confirm:
#             return "Passwords do not match"
#         password = (str(password))
#         password = hashlib.sha1(password.encode()).hexdigest()
#         # Store the user's email and password in the database
#         conn = sqlite3.connect(DATABASE)
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
#         conn.commit()
#         conn.close()

#         # Redirect the user to the login page
#         return redirect(url_for('login'))


#     return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Check if the email and password are correct
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        password = hashlib.sha1(password.encode()).hexdigest()
        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?", (email, password)
        )
        user = cur.fetchone()
        conn.close()

        # Redirect the user to the main page
        if not user:
            # Display an error message
            error_msg = "Incorrect email or password"
            return render_template("login.html", error_msg=error_msg)

        session["logged_in"] = True
        return redirect(url_for("main_page"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session["logged_in"] = False
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password1"]
        password_confirm = request.form["password2"]

        if password != password_confirm:
            return "Passwords do not match"

        password = hashlib.sha1(password.encode()).hexdigest()

        # Check if the email is already registered
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT email FROM users WHERE email=?", (email,))
        result = cur.fetchone()
        conn.close()

        if result is not None:
            return render_template("register.html")

        # Store the user's email and password in the database
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)", (email, password)
        )
        conn.commit()
        conn.close()

        # Redirect the user to the login page
        return redirect(url_for("login"))

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
