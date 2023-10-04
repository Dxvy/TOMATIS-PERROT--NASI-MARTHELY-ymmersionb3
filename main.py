from flask import Flask, jsonify, render_template
import sqlalchemy as db
import json

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

schema = 'trashcans'
engine = db.create_engine(f'mysql://root:root@localhost:3306/{schema}')
metadata = db.MetaData(schema=schema)


# with open("backend/trashcans.json", "r") as read_file:
#     data = json.load(read_file)


@app.route('/', methods=['GET'])
def get_all_products_data():
    # cursor = mysql.connection.cursor()
    # cursor.execute("SELECT * FROM products")
    # data = cursor.fetchall()
    # cursor.close()
    # return render_template('index.html', products=data)
    return render_template('index.html', products=data)


# @app.route('/<int:product_id>', methods=['GET'])
# def get_data_by_id(product_id):
#     item = next((item for item in data if item["product_id"] == product_id), None)
#     if item is None:
#         return render_template('error_page.html')
#     return render_template('product_page.html', product=item)


@app.route('/cart', methods=['GET'])
def get_cart():
    return render_template('cart_page.html')


if __name__ == "__main__":
    app.run(debug=True)
