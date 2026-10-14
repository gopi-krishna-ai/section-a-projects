import sqlite3
import os
from werkzeug.security import generate_password_hash

db_path = os.path.join('database', 'agrimitra.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Check if old admin exists
c.execute('SELECT * FROM users WHERE userid = ?', ('admin',))
old_admin = c.fetchone()

# Check if new admin exists
c.execute('SELECT * FROM users WHERE userid = ?', ('admin@agrimitra',))
new_admin = c.fetchone()

pw_hash = generate_password_hash('admin@123')

if old_admin and not new_admin:
    # Rename old admin
    c.execute('UPDATE users SET userid = ?, password = ? WHERE userid = ?', ('admin@agrimitra', pw_hash, 'admin'))
    print("Renamed existing 'admin' to 'admin@agrimitra' and updated password.")
elif new_admin:
    # Update existing new admin
    c.execute('UPDATE users SET password = ? WHERE userid = ?', (pw_hash, 'admin@agrimitra'))
    print("Updated password for existing 'admin@agrimitra'.")
else:
    # Create new admin
    c.execute('INSERT INTO users (fullname, userid, email, phone, password, language) VALUES (?, ?, ?, ?, ?, ?)', 
              ('System Admin', 'admin@agrimitra', 'admin@agrimitra.local', '0000000000', pw_hash, 'en'))
    print("Created new 'admin@agrimitra' user.")

conn.commit()
conn.close()
