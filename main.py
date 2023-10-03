from flask import Flask, jsonify, render_template
import json

app = Flask(__name__, template_folder="frontend/templates")

with open('backend/trashcans.json', 'r', encoding="utf-8") as f:
    data = json.load(f)


@app.route('/', methods=['GET'])
def get_all_data():
    return render_template('index.html', data=data)


@app.route('/<int:product_id>', methods=['GET'])
def get_data_by_id(product_id):
    item = next((item for item in data if item["product_id"] == product_id), None)
    if item is None:
        return render_template('error_page.html')
    return render_template('product_page.html', product=item)


@app.route('/cart', methods=['GET'])
def get_cart():
    return render_template('cart_page.html')


if __name__ == "__main__":
    app.run(debug=True)
