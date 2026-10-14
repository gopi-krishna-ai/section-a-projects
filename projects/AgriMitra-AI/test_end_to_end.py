import sqlite3
import urllib.request
import urllib.parse
import json
from http.cookiejar import CookieJar

BASE_URL = 'http://127.0.0.1:5000'

def create_session():
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    return opener

# 1. Direct DB Setup for User and Product
print("Setting up test data...")
conn = sqlite3.connect('database/agrimitra.db')
c = conn.cursor()

c.execute('SELECT id FROM users WHERE userid = "gopi_123"')
user = c.fetchone()
if not user:
    c.execute('INSERT INTO users (fullname, userid, password, email, phone) VALUES (?, ?, ?, ?, ?)', 
              ('Gopi Krishna Test', 'gopi_123', 'testpass123', 'gopi@test.com', '1234567890'))
    conn.commit()
    user_id = c.lastrowid
else:
    user_id = user[0]

c.execute('SELECT id, price FROM products WHERE item_name LIKE "%Coffee%"')
product = c.fetchone()
if not product:
    c.execute('INSERT INTO products (item_type, item_name, seller, description, price, image_url, stock, discount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              ('seed', 'Coffee Beans', 'Admin', 'Premium Coffee', 1500, '/static/images/coffee.jpg', 100, 0))
    conn.commit()
    product_id = c.lastrowid
    product_price = 1500
else:
    product_id = product[0]
    product_price = product[1]

conn.close()

# 2. Login as gopi_123
print("Logging in as gopi_123...")
user_opener = create_session()
req = urllib.request.Request(f"{BASE_URL}/api/login", 
                             data=json.dumps({"userid": "gopi_123", "password": "testpass123"}).encode('utf-8'),
                             headers={'Content-Type': 'application/json'})
res = user_opener.open(req)
print("Login success:", json.loads(res.read().decode('utf-8')).get('success'))

# 3. Simulate Checkout (with auto-grabbed location)
print("Simulating checkout with Map Location...")
checkout_payload = {
    "cart": [{"product_id": product_id, "quantity": 2, "price": product_price}],
    "address": "Coffee Estate, Chikmagalur (13.3153, 75.7754)"
}
req = urllib.request.Request(f"{BASE_URL}/api/checkout", 
                             data=json.dumps(checkout_payload).encode('utf-8'),
                             headers={'Content-Type': 'application/json'})
res = user_opener.open(req)
print("Checkout Response:", json.loads(res.read().decode('utf-8')))

# 4. Login as Admin
print("Logging in as Admin...")
admin_opener = create_session()
req = urllib.request.Request(f"{BASE_URL}/api/admin/login", 
                             data=json.dumps({"userid": "admin@agrimitra", "password": "admin@123"}).encode('utf-8'),
                             headers={'Content-Type': 'application/json'})
admin_opener.open(req)

# 5. Fetch Admin Orders
print("Fetching Admin Orders...")
req = urllib.request.Request(f"{BASE_URL}/api/admin/orders")
res = admin_opener.open(req)
orders_data = json.loads(res.read().decode('utf-8'))

print("\\n--- ADMIN ORDERS VISIBLE ---")
for o in orders_data.get('orders', []):
    print(f"Order #{o['id']} | Customer: {o['user']} | Total: Rs {o['total_amount']} | Status: {o['status']}")
    print(f"Location: {o['delivery_address']}")
    for i in o['items']:
        print(f"  - {i['quantity']}kg {i['product_name']}")
    print("-" * 30)

