import pandas as pd
import sqlite3

# === STEP 1: LOAD CSV ===
csv_path = "products.csv"  # Make sure this file is in the same folder
df = pd.read_csv(csv_path)

# === STEP 2: CONNECT TO SQLITE DB ===
db_path = "products_database.db"  # This file will be created
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# === STEP 3: CREATE TABLE ===
cursor.execute("DROP TABLE IF EXISTS products")  # Optional: clears previous data
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        cost REAL,
        category TEXT,
        name TEXT,
        brand TEXT,
        retail_price REAL,
        department TEXT,
        sku TEXT,
        distribution_center_id INTEGER
    )
""")

# === STEP 4: INSERT CSV DATA INTO TABLE ===
df.to_sql("products", conn, if_exists="append", index=False)
print("✅ Data inserted successfully.")

# === STEP 5: SAMPLE QUERIES ===

# 1. Count total rows
cursor.execute("SELECT COUNT(*) FROM products")
total_rows = cursor.fetchone()[0]
print(f"Total rows: {total_rows}")

# 2. Show 5 sample products
print("\nSample Products:")
sample_rows = cursor.execute("SELECT id, name, cost, brand, retail_price FROM products LIMIT 5").fetchall()
for row in sample_rows:
    print(row)

# 3. Find most expensive product
most_expensive = cursor.execute("""
    SELECT name, retail_price FROM products
    ORDER BY retail_price DESC LIMIT 1
""").fetchone()
print(f"\n💰 Most expensive product: {most_expensive[0]} (${most_expensive[1]})")

# 4. Average cost by category
avg_costs = cursor.execute("""
    SELECT category, ROUND(AVG(cost), 2) as avg_cost
    FROM products
    GROUP BY category
    ORDER BY avg_cost DESC
    LIMIT 5
""").fetchall()
print("\nTop 5 categories by average cost:")
for cat in avg_costs:
    print(f"{cat[0]} - ${cat[1]}")

# === STEP 6: CLOSE CONNECTION ===
conn.close()
