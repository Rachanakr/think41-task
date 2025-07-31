from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Updated DB path
DB_PATH = os.path.join(os.path.dirname(__file__), 'products_database.db')

# GET all products
@app.route('/api/products', methods=['GET'])
def get_all_products():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")  # Update 'products' if your table name is different
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET a product by ID
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

# Start Flask server
if __name__ == '__main__':
    app.run(debug=True)
