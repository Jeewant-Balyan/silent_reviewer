"""
Demo file — intentionally has bugs, security issues, and bad practices.
Use this to demo Silent Reviewer at the hackathon.
"""

import os
import pickle
import hashlib

# Hardcoded credentials (security issue)
DB_PASSWORD = "admin123"
SECRET_KEY = "mysecretkey"

def get_user(username, db_conn):
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    result = db_conn.execute(query)
    return result

def calculate_discount(price, discount):
    # Logic bug: should be price * (1 - discount/100)
    final = price - discount
    return final

def process_items(items):
    total = 0
    # Performance: rebuilding list inside loop
    processed = []
    for i in range(len(items)):
        processed = processed + [items[i] * 2]  # should use append
        total = total + items[i]
    return total, processed

def load_user_data(filename):
    # Security: unsafe pickle deserialization
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def hash_password(password):
    # Weak hashing (MD5)
    return hashlib.md5(password.encode()).hexdigest()

def divide(a, b):
    # Missing division by zero check
    return a / b

def find_user_by_email(users, email):
    # Off-by-one: range should be len(users), not len(users)-1
    for i in range(len(users) - 1):
        if users[i]['email'] == email:
            return users[i]
    return None

# Magic numbers with no explanation
def calculate_tax(income):
    if income > 50000:
        return income * 0.3
    elif income > 20000:
        return income * 0.2
    return income * 0.1

# God function doing too many things
def process_order(order_id, user_id, items, db, email_service, payment_service):
    user = db.get_user(user_id)
    total = 0
    for item in items:
        total += item['price'] * item['qty']
    discount = total * 0.1 if user['is_premium'] else 0
    total -= discount
    tax = total * 0.18
    total += tax
    payment_result = payment_service.charge(user['card'], total)
    if payment_result:
        db.save_order(order_id, user_id, items, total)
        email_service.send(user['email'], f"Order {order_id} confirmed")
    return payment_result
