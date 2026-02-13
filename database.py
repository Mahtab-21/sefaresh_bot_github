import sqlite3
from datetime import datetime

conn = sqlite3.connect("orders.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY,
    product TEXT,
    color TEXT,
    qty INTEGER,
    name TEXT,
    phone TEXT,
    address TEXT,
    postal TEXT,
    price INTEGER,
    paid INTEGER DEFAULT 0,
    authority TEXT,
    date TEXT
)
""")

conn.commit()


def save_order(data):
    cursor.execute("""
    INSERT INTO orders
    (id, product, color, qty, name, phone, address, postal, price, paid, authority, date)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["id"],
        data["product"],
        data["color"],
        data["qty"],
        data["name"],
        data["phone"],
        data["address"],
        data["postal"],
        data["price"],
        0,
        None,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()


def get_order(order_id):
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    return cursor.fetchone()


def set_authority(order_id, authority):
    cursor.execute("UPDATE orders SET authority=? WHERE id=?", (authority, order_id))
    conn.commit()


def set_paid(order_id):
    cursor.execute("UPDATE orders SET paid=1 WHERE id=?", (order_id,))
    conn.commit()
