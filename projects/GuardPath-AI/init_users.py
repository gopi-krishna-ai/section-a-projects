import os
import json

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI'
users_file = os.path.join(base_dir, 'data', 'users.json')

initial_users = {
    'admin': {'password': 'admin', 'role': 'admin', 'name': 'System Admin', 'email': 'admin@guardpath.local'},
    'passenger1': {'password': 'pass1', 'role': 'passenger', 'name': 'Alice', 'email': 'alice@example.com'},
    'passenger2': {'password': 'pass2', 'role': 'passenger', 'name': 'Bob', 'email': 'bob@example.com'}
}

# Create users.json if it doesn't exist
if not os.path.exists(users_file):
    os.makedirs(os.path.dirname(users_file), exist_ok=True)
    with open(users_file, 'w') as f:
        json.dump(initial_users, f, indent=4)
