"""
AI-Assisted Smart Study Planner - flat-file storage.

No database server is used (per the project brief) - subject data and
a short missed-session log are kept in a single local JSON file.
"""

import json
import os
import threading
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_PATH = os.path.join(DATA_DIR, "users.json")

os.makedirs(DATA_DIR, exist_ok=True)

_lock = threading.Lock()

DEFAULT_STORE = {
    "subjects": {},
    "settings": {"daily_hours": 4},
    "missed_log": [],
    "session_actions": {},
}

def _get_store_path(username):
    return os.path.join(DATA_DIR, f"{username}_store.json")

def load_store(username="default"):
    path = _get_store_path(username)
    with _lock:
        if not os.path.exists(path):
            return json.loads(json.dumps(DEFAULT_STORE))
        with open(path) as f:
            data = json.load(f)
        data.setdefault("subjects", {})
        data.setdefault("settings", {"daily_hours": 4})
        data.setdefault("missed_log", [])
        data.setdefault("session_actions", {})
        return data

def save_store(data, username="default"):
    path = _get_store_path(username)
    with _lock:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

def load_users():
    with _lock:
        if not os.path.exists(USERS_PATH):
            return {}
        with open(USERS_PATH) as f:
            return json.load(f)

def save_users(users_data):
    with _lock:
        with open(USERS_PATH, "w") as f:
            json.dump(users_data, f, indent=2)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    users[username] = hashed_pw
    save_users(users)
    return True

def verify_user(username, password):
    users = load_users()
    if username not in users:
        return False
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    return users[username] == hashed_pw
