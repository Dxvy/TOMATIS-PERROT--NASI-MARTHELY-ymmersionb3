from flask import Flask, jsonify, render_template, request
from backend.api import DataBase
from backend.utils import convert_to_base64
from sqlalchemy.orm import Session

db = DataBase('root', '', 'localhost', '3306', 'trashtalk')

db.connect()
session = Session()
session.begin()

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")


# main route, needs all products
# TODO: add recommendation system and search bar
@app.route('/', methods=['GET'])
def display_all_products_data():
    items = db.get_all_products()
    recommendations = db.get_recommended_products()
    return render_template('homepage.jinja', products=items, recommendations=recommendations)


# product route, needs all product info
@app.route('/<int:product_id>', methods=['GET'])
def get_data_by_id(product_id):
    item = db.get_product_by_id(product_id)
    return render_template('product_page.jinja', product=item)


# cart page, needs all products in cart from the local storage
@app.route('/cart', methods=['GET'])
def get_cart():
    return render_template('cart_page.jinja')


# login route
@app.route('/login', methods=['GET'])
def login():
    return render_template('login_page.jinja')


# register route
@app.route('/register', methods=['GET'])
def register():
    return render_template('register_page.jinja')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    lastname = request.form.get('lastname')
    phone = request.form.get('phone')
    type = request.form.get('type')
    company = request.form.get('company')
    password = request.form.get('password')
    if db.insert_user(email, name, lastname, phone, type, company, password):
        return render_template('login_page.jinja')
    return render_template('register_page.jinja')


if __name__ == "__main__":
    app.run(debug=True)
