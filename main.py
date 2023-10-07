from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash
from backend.api import DataBase
from backend.utils import *
from flask_session import Session
from datetime import timedelta
import os

db = DataBase('root', '', 'localhost', '3306', 'trashtalk')

db.connect()

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = './frontend/static/images'
Session(app)

app.secret_key = 'super secret key'
app.permanent_session_lifetime = timedelta(minutes=30)


# main route, needs all products
# TODO: add recommendation system
@app.route('/', methods=['GET'])
def display_all_products_data():
    if 'guid' not in session:
        redirect(url_for('login'))
        return render_template('login_page.jinja')
    items = db.get_all_products()

    if request.args.get("filter") is not None:
        filter_by_price(items, request.args.get('select-price'))
        filter_by_type(items, request.args.get('select-type'))
        filter_by_size(items, request.args.get('select-size'))
    recommendations = db.get_recommended_products()
    return render_template('homepage.jinja', products=items, recommendations=recommendations)


# search route, needs all products that match the search string
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'guid' not in session:
        redirect(url_for('login'))
        return render_template('login_page.jinja')

    if request.method == 'POST':
        product_string = request.args.get('product')
        filter_filter = request.form.get('filter')
        select_price = request.form.get('select-price')
        select_type = request.form.get('select-type')
        select_size = request.form.get('select-size')
        return redirect(url_for('search', product=product_string, filter=filter_filter, select_price=select_price,
                                select_type=select_type, select_size=select_size))

    product_string = request.args.get('product')

    items = db.get_products_by_string(product_string)

    if request.args.get("filter") is not None:
        filter_by_price(items, request.args.get('select_price'))
        filter_by_type(items, request.args.get('select_type'))
        filter_by_size(items, request.args.get('select_size'))

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


# cart order
@app.route('/cart', methods=['POST'])
def post_cart():
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


@app.route('/marketplace', methods=['GET', 'POST'])
def marketplace_post():
    if 'guid' not in session:
        redirect(url_for('login'))
        return render_template('login_page.jinja')
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type-list')
        size = request.form.get('size-list')
        sorting = request.form.get('sorting')
        color = request.form.get('color')
        price = request.form.get('price')
        description = request.form.get('description')
        quantity = request.form.get('quantity')

        if 'img1-product' in request.files and 'img2-product' in request.files and 'img3-product' in request.files:
            img1 = request.files['img1-product']
            img2 = request.files['img2-product']
            img3 = request.files['img3-product']
            result = db.add_product(name, type, size, sorting, color, price, description, quantity)
            if result:
                img1.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{result}-1.jpeg"))
                img2.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{result}-2.jpeg"))
                img3.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{result}-3.jpeg"))
                return redirect(url_for('display_all_products_data'))
    return render_template('marketplace_page.jinja')


@app.route('/api/get_row/<int:item_id>')
def get_row(item_id):
    item = db.get_product_by_id(item_id)

    # Check if item is not None
    if item is not None:
        # Convert the 'Row' object to a dictionary
        item_dict = {
            'id': item.id,
            'name': item.name,
            'type': item.type,
            'size': item.size,
            'sorting': item.sorting,
            'color': item.color,
            'price': item.price,
            'description': item.description
        }

        return jsonify(item_dict), 200
    else:
        return jsonify({'error': 'Item not found'}), 404


if __name__ == "__main__":
    app.run(debug=True)
