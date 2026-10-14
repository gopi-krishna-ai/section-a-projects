"""
Simple flat-file user authentication for StudyMind.
"""
import json
import os
import hashlib
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_PATH = os.path.join(DATA_DIR, "users.json")

os.makedirs(DATA_DIR, exist_ok=True)
_lock = threading.Lock()

def _load_users():
    with _lock:
        if not os.path.exists(USERS_PATH):
            return {}
        with open(USERS_PATH) as f:
            return json.load(f)

def _save_users(data):
    with _lock:
        with open(USERS_PATH, "w") as f:
            json.dump(data, f, indent=2)

def register_user(username, password):
    users = _load_users()
    if username in users:
        return False
    users[username] = hashlib.sha256(password.encode()).hexdigest()
    _save_users(users)
    return True

def verify_user(username, password):
    users = _load_users()
    if username not in users:
        return False
    return users[username] == hashlib.sha256(password.encode()).hexdigest()
