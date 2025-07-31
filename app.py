from flask import Flask, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'products_database.db')

# 🟢 Products List View (HTML page)
@app.route('/')
def home():
    return render_template("index.html")

# 🟢 Product Detail View (HTML page)
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    return render_template("detail.html", product_id=product_id)

# 🔁 API Endpoint: All products
@app.route('/api/products', methods=['GET'])
def get_all_products():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🔁 API Endpoint: Product by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            product = dict(zip(columns, row))
            return jsonify(product), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
