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

conn = sqlite3.connect('database/agrimitra.db')
c = conn.cursor()

c.execute('SELECT id FROM users WHERE userid = "gopi_123"')
user = c.fetchone()
if not user:
    c.execute('INSERT INTO users (fullname, userid, password, email, phone) VALUES (?, ?, ?, ?, ?)', 
              ('Gopi Krishna', 'gopi_123', 'test', 'gopi@test.com', '123'))
    conn.commit()
    user_id = c.lastrowid
else:
    user_id = user[0]

c.execute('SELECT id FROM products WHERE item_name LIKE "%Coffee%"')
product = c.fetchone()
if not product:
    c.execute('INSERT INTO products (item_type, item_name, seller, description, price, image_url, stock, discount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              ('seed', 'Coffee Beans', 'Admin', 'Premium Coffee', 1500, '/static/images/coffee.jpg', 100, 0))
    conn.commit()
    product_id = c.lastrowid
else:
    product_id = product[0]

# Insert order
c.execute('INSERT INTO orders (user_id, total_amount, status, delivery_address) VALUES (?, ?, ?, ?)',
          (user_id, 3000, 'Pending', 'Coffee Estate, Chikmagalur (13.31, 75.77)'))
order_id = c.lastrowid
c.execute('INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
          (order_id, product_id, 2, 1500))
conn.commit()
conn.close()

admin_opener = create_session()
req = urllib.request.Request(f'{BASE_URL}/api/admin/login', data=json.dumps({'userid': 'admin@agrimitra', 'password': 'admin@123'}).encode('utf-8'), headers={'Content-Type': 'application/json'})
admin_opener.open(req)

req = urllib.request.Request(f'{BASE_URL}/api/admin/orders')
res = admin_opener.open(req)
orders_data = json.loads(res.read().decode('utf-8'))

print("\\n✅ ADMIN VERIFICATION RESULTS:")
for o in orders_data.get('orders', []):
    print(f"Order #{o['id']} | Customer: {o['user']} | Status: {o['status']}")
    print(f"Location grabbed: {o['delivery_address']}")
    for i in o['items']:
        print(f"  - {i['quantity']}kg {i['product_name']}")
    print("-" * 30)
