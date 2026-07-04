from passlib.context import CryptContext
import json
import os
import streamlit as st

USER_FILE = "linguistix_users.json"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEMO_FALLBACK_PASSWORDS = {
    "hie": "123456",
    "testuser": "123456",
    "demo": "demo123",
}


def get_storage_path(username=None):
    """Return the path for user-specific storage or default storage."""
    if username:
        return f"data_user_{username}.json"
    return "linguistix_temp_data.json"

@st.cache_data(show_spinner=False)
def load_data(username=None):
    """Load history, favorites, and phrasebook from a user-specific JSON file."""
    path = get_storage_path(username)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Storage Load Error for {username if username else 'guest'}: {e}")
    return {"history": [], "favorites": [], "phrasebook": []}

def save_data(history, favorites, phrasebook=[], username=None):
    """Save history, favorites, and phrasebook to a user-specific JSON file."""
    st.cache_data.clear()
    path = get_storage_path(username)
    try:
        data = {
            "history": history[-50:], # Limit history to last 50
            "favorites": favorites,
            "phrasebook": phrasebook
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Storage Save Error for {username if username else 'guest'}: {e}")

@st.cache_data(show_spinner=False)
def load_users():
    """Load users from a local JSON file and ensure new format."""
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
                updated = False

                # Migration: Convert old format {"user": "hash"} to {"user": {"password": "hash", "email": ""}}
                for username, data in list(users.items()):
                    if isinstance(data, str):
                        users[username] = {"password": data, "email": ""}
                        updated = True

                # Ensure demo accounts use a known working password for local development.
                for username, fallback_password in DEMO_FALLBACK_PASSWORDS.items():
                    if username in users and isinstance(users[username], dict):
                        stored = users[username].get("password", "")
                        if not stored:
                            users[username]["password"] = hash_password(fallback_password)
                            updated = True
                        else:
                            try:
                                if not verify_password(fallback_password, stored):
                                    users[username]["password"] = hash_password(fallback_password)
                                    updated = True
                            except Exception:
                                users[username]["password"] = hash_password(fallback_password)
                                updated = True

                if updated:
                    save_users(users)
                return users
        except Exception as e:
            print(f"User Load Error: {e}")
    return {}

def find_user(identifier, users):
    """Find a user by username or email."""
    # Check username first
    if identifier in users:
        return identifier, users[identifier]
    # Check email
    for username, data in users.items():
        if data.get("email") == identifier:
            return username, data
    return None, None

def save_users(users):
    """Save users to a local JSON file."""
    st.cache_data.clear()
    try:
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"User Save Error: {e}")

def get_remembered_user():
    """Check if a user is remembered on this machine."""
    if os.path.exists(".remember_me"):
        try:
            with open(".remember_me", "r") as f:
                return f.read().strip()
        except: pass
    return None

def set_remember_me(username, state=True):
    """Set or clear the remember me flag."""
    if state and username:
        with open(".remember_me", "w") as f:
            f.write(username)
    elif os.path.exists(".remember_me"):
        os.remove(".remember_me")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    if not password or not hashed:
        return False
    try:
        return pwd_context.verify(password, hashed)
    except Exception:
        return False


def authenticate_user(identifier, password, users):
    """Authenticate a user by username or email and migrate legacy/demo credentials when needed."""
    username, user_data = find_user(identifier, users)
    if not user_data:
        return None, None, "User not found"

    stored_password = user_data.get("password")
    if isinstance(stored_password, str) and verify_password(password, stored_password):
        return username, user_data, None

    if isinstance(stored_password, str) and stored_password == password:
        users[username]["password"] = hash_password(password)
        save_users(users)
        return username, users[username], None

    if username in DEMO_FALLBACK_PASSWORDS and password == DEMO_FALLBACK_PASSWORDS[username]:
        users[username]["password"] = hash_password(password)
        save_users(users)
        return username, users[username], None

    return None, None, "Invalid credentials."


def register_user(username, email, password, users):
    """Create a user record with a hashed password."""
    username = (username or "").strip()
    email = (email or "").strip().lower()
    if not username or not email or not password:
        raise ValueError("Please enter a username, email, and password.")
    if username in users:
        raise ValueError("Username already taken")
    if any(isinstance(data, dict) and data.get("email", "").lower() == email for data in users.values()):
        raise ValueError("Email already registered")
    users[username] = {"password": hash_password(password), "email": email}
    save_users(users)
    return users
