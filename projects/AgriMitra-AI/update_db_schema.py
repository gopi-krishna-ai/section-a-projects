import sqlite3
import os

db_path = os.path.join('database', 'agrimitra.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

# 1. Add stock and discount to products
try:
    c.execute('ALTER TABLE products ADD COLUMN stock INTEGER DEFAULT 100')
    print("Added stock column")
except sqlite3.OperationalError:
    pass # column exists

try:
    c.execute('ALTER TABLE products ADD COLUMN discount INTEGER DEFAULT 0')
    print("Added discount column")
except sqlite3.OperationalError:
    pass

# 2. Create Orders table
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# 3. Create OrderItems table
c.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
''')

conn.commit()
conn.close()
print("Database schema updated successfully.")
