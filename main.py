from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash

from backend.api import DataBase
from backend.utils import *
from sqlalchemy.orm import Session
from flask_session import Session
from datetime import timedelta

db = DataBase('root', '', 'localhost', '3306', 'trashtalk')

db.connect()

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.secret_key = 'super secret key'
app.permanent_session_lifetime = timedelta(minutes=30)


# main route, needs all products
# TODO: add recommendation system and search bar
@app.route('/', methods=['GET'])
def display_all_products_data():
    if 'guid' not in session:
        redirect(url_for('login'))
        return render_template('login_page.jinja')
    items = db.get_all_products()
    recommendations = db.get_recommended_products()
    return render_template('homepage.jinja', products=items, recommendations=recommendations)


@app.route('/search', methods=['GET'])
def search():
    product_string = request.args.get('product', '')
    print(product_string)
    items = db.get_products_by_string(product_string)
    return render_template('homepage.jinja', products=items, recommendations=None)


# product route, needs all product info
@app.route('/<int:product_id>', methods=['GET'])
def get_data_by_id(product_id):
    if 'guid' not in session:
        redirect(url_for('login'))
        return render_template('login_page.jinja')
    item = db.get_product_by_id(product_id)
    return render_template('product_page.jinja', product=item)


# cart page, needs all products in cart from the local storage
@app.route('/cart', methods=['GET'])
def get_cart():
    if 'guid' not in session:
        redirect(url_for('login'))
        return render_template('login_page.jinja')
    return render_template('cart_page.jinja')


# login route
@app.route('/login', methods=['GET'])
def login():
    if 'guid' in session:
        return redirect(url_for('display_all_products_data'))
    return render_template('login_page.jinja')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    if db.check_login(email, password):
        session['guid'] = db.get_user_guid(email)
        return redirect(url_for('display_all_products_data'))
    flash('Email address or password is incorrect')
    return render_template('login_page.jinja')


# register route
@app.route('/register', methods=['GET'])
def register():
    if 'guid' in session:
        return redirect(url_for('display_all_products_data'))
    return render_template('register_page.jinja')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    lastname = request.form.get('lastname')
    phone = request.form.get('tel')
    profile = request.form.get('profile')
    company = request.form.get('company')
    password = generate_password_hash(request.form.get('password'))
    if db.insert_user(email, name, lastname, phone, profile, company, password):
        return redirect(url_for('login'))
    flash('Email address already exists')
    return render_template('register_page.jinja')


# logout route
@app.route('/logout', methods=['GET'])
def logout():
    if 'guid' not in session:
        redirect(url_for('login'))
        return render_template('login_page.jinja')
    session.pop('guid', None)
    return redirect(url_for('login'))


# # marketplace route
# @app.route('/marketplace', methods=['GET'])
# def marketplace():
#     if 'guid' not in session:
#         redirect(url_for('login'))
#         return render_template('login_page.jinja')
#     return render_template('marketplace_page.jinja')
#
#
# @app.route('/marketplace', methods=['POST'])
# def marketplace_post():
#     if 'guid' not in session:
#         redirect(url_for('login'))
#         return render_template('login_page.jinja')
#     return render_template('marketplace_page.jinja')


if __name__ == "__main__":
    app.run(debug=True)
