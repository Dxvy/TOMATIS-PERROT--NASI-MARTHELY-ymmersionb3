from flask import Flask, jsonify, render_template
# from flask_mysqldb import MySQL
import json

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


@app.route('/cart', methods=['GET'])
def get_cart():
    return render_template('cart_page.html')


if __name__ == "__main__":
    app.run(debug=True)
